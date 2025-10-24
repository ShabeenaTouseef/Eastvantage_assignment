import argparse
from sql_solution import sql_solution
from pandas_solution import pandas_solution

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--method", required=True, choices=["sql","pandas"])
    parser.add_argument("--out", required=True)
    parser.add_argument("--min-age", type=int, default=18)
    parser.add_argument("--max-age", type=int, default=35)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.method == "sql":
        sql_solution(db_path=args.db, out_path=args.out, min_age=args.min_age, max_age=args.max_age)
    else:
        pandas_solution(db_path=args.db, out_path=args.out, min_age=args.min_age, max_age=args.max_age)
