from __future__ import annotations
import sys
from decimal import Decimal, getcontext, ROUND_FLOOR
from typing import List, Dict, Optional

# set high precision to avoid any intermediate rounding issues
getcontext().prec = 28

MONTHS = [
    "JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE",
    "JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"
]
month_index: Dict[str,int] = {m:i for i,m in enumerate(MONTHS)}
for m in MONTHS:
    month_index[m[:3]] = month_index[m]

def parse_percent_token_decimal(token: str) -> Decimal:
    """
    Parse percentage token into Decimal percent (e.g. "4.00%" -> Decimal('4.00')).
    Returns Decimal('0') on malformed token.
    """
    if token is None:
        return Decimal('0')
    t = token.strip()
    if t.endswith('%'):
        t = t[:-1]
    # strip plus sign if present
    if t.startswith('+'):
        t = t[1:]
    try:
        return Decimal(t)
    except Exception:
        return Decimal('0')

def floor_decimal_to_int(d: Decimal) -> int:
    """
    Floor Decimal d to the nearest lower integer and return int.
    Uses ROUND_FLOOR to match math.floor behaviour for positives/negatives.
    """
    return int(d.to_integral_value(rounding=ROUND_FLOOR))

def floor_list_decimals(vals: List[Decimal]) -> List[int]:
    return [floor_decimal_to_int(v) for v in vals]

def print_triplet_ints(vals: List[int]) -> None:
    a, b, c = int(vals[0]), int(vals[1]), int(vals[2])
    print(f"{a} {b} {c}")

def normalize_month_token(tok: str) -> Optional[str]:
    if not tok:
        return None
    t = tok.strip().upper()
    if t in month_index:
        return MONTHS[month_index[t]]
    t_clean = ''.join(ch for ch in t if ch.isalpha())
    if t_clean in month_index:
        return MONTHS[month_index[t_clean]]
    return None

def process_commands(lines: List[str]) -> None:
    """
    Process commands with Decimal arithmetic and strict validation.
    Exits with sys.exit(1) if ALLOCATE rule is violated.
    """
    saw_allocate = False

    initial_alloc: Optional[List[Decimal]] = None
    target_percents: Optional[List[Decimal]] = None  # fractions e.g. Decimal('0.6')
    sip: List[Decimal] = [Decimal('0'), Decimal('0'), Decimal('0')]
    current: Optional[List[Decimal]] = None
    snapshots: Dict[str, List[int]] = {}
    last_rebalance: Optional[List[int]] = None

    for raw in lines:
        if raw is None:
            continue
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if not parts:
            continue
        cmd = parts[0].upper()

        # Strict validation: ALLOCATE must be seen before any other action except comments/blanks.
        if not saw_allocate and cmd != "ALLOCATE":
            # If the line is a benign 'COMMENT' or something else that's allowed skip, but per strict rule, we exit.
            # Exiting silently with non-zero code to signal invalid input ordering.
            sys.exit(1)

        if cmd == "ALLOCATE":
            # Format: ALLOCATE E D G
            if len(parts) < 4:
                sys.exit(1)  # malformed ALLOCATE
            try:
                e = Decimal(parts[1])
                d = Decimal(parts[2])
                g = Decimal(parts[3])
            except Exception:
                sys.exit(1)
            initial_alloc = [e, d, g]
            total = e + d + g
            if total <= Decimal('0'):
                target_percents = [Decimal('0'), Decimal('0'), Decimal('0')]
            else:
                # fractions: exact decimals
                target_percents = [ (e / total), (d / total), (g / total) ]
            current = [e, d, g]
            saw_allocate = True

        elif cmd == "SIP":
            # Format: SIP E D G
            if len(parts) < 4:
                sys.exit(1)
            try:
                sip = [Decimal(parts[1]), Decimal(parts[2]), Decimal(parts[3])]
            except Exception:
                sys.exit(1)

        elif cmd == "CHANGE":
            # Format: CHANGE p_e p_d p_g MONTH
            if len(parts) < 5:
                sys.exit(1)
            p_e = parse_percent_token_decimal(parts[1])
            p_d = parse_percent_token_decimal(parts[2])
            p_g = parse_percent_token_decimal(parts[3])
            month_token = " ".join(parts[4:]).strip()
            normalized_month = normalize_month_token(month_token)
            if current is None or normalized_month is None:
                sys.exit(1)

            idx = month_index[normalized_month]

            # percent as fraction: Decimal(p)/100
            pe_frac = p_e / Decimal('100')
            pd_frac = p_d / Decimal('100')
            pg_frac = p_g / Decimal('100')

            if idx == 0:
                after_market = [
                    current[0] * (Decimal('1') + pe_frac),
                    current[1] * (Decimal('1') + pd_frac),
                    current[2] * (Decimal('1') + pg_frac),
                ]
            else:
                after_sip = [current[0] + sip[0], current[1] + sip[1], current[2] + sip[2]]
                after_market = [
                    after_sip[0] * (Decimal('1') + pe_frac),
                    after_sip[1] * (Decimal('1') + pd_frac),
                    after_sip[2] * (Decimal('1') + pg_frac),
                ]

            # floor to ints and store snapshot
            after_market_floored_ints = floor_list_decimals(after_market)
            snapshots[normalized_month] = after_market_floored_ints.copy()

            # If June or December: compulsory rebalance
            if idx == 5 or idx == 11:
                total_after = sum(after_market_floored_ints)  # int sum
                total_after_dec = Decimal(total_after)
                if target_percents is None:
                    last_rebalance = None
                else:
                    reb_e = floor_decimal_to_int(total_after_dec * target_percents[0])
                    reb_d = floor_decimal_to_int(total_after_dec * target_percents[1])
                    reb_g = floor_decimal_to_int(total_after_dec * target_percents[2])
                    last_rebalance = [reb_e, reb_d, reb_g]
                    current = [Decimal(reb_e), Decimal(reb_d), Decimal(reb_g)]
            else:
                current = [Decimal(after_market_floored_ints[0]),
                           Decimal(after_market_floored_ints[1]),
                           Decimal(after_market_floored_ints[2])]

        elif cmd == "BALANCE":
            # Format: BALANCE MONTH
            if len(parts) < 2:
                sys.exit(1)
            month_token = " ".join(parts[1:]).strip()
            normalized_month = normalize_month_token(month_token)
            if normalized_month and normalized_month in snapshots:
                print_triplet_ints(snapshots[normalized_month])
            else:
                if current is None:
                    print("CANNOT_BALANCE")
                else:
                    print_triplet_ints(floor_list_decimals(current))

        elif cmd == "REBALANCE":
            if last_rebalance is None:
                print("CANNOT_REBALANCE")
            else:
                print_triplet_ints(last_rebalance)

        else:
            # Unknown command -> treat as malformed under strict validation
            sys.exit(1)

    # End for: final validation - ensure ALLOCATE was present (saw_allocate)
    if not saw_allocate:
        sys.exit(1)

def main() -> None:
    if len(sys.argv) < 2:
        # missing input file -> error
        sys.exit(1)
    input_file = sys.argv[1]
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        sys.exit(1)

    process_commands(lines)

if __name__ == "__main__":
    main()
