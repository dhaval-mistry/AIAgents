"""Live retrieval evaluation. Each question makes a billable Titan request."""
import argparse
import json
from pathlib import Path
from rag.vectors import LocalVectors
from rag.chat import retrieval_question


# Run labeled questions against live retrieval and report whether an expected
# source title appears among the top matches; this evaluates retrieval, not prose.
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cases',type=Path,help='JSON list of questions and expected source titles')
    args=parser.parse_args()
    cases=json.loads(args.cases.read_text(encoding='utf-8'))
    library=LocalVectors()
    passed=0
    for case in cases:
        hits=library.search(retrieval_question(case['question'],case.get('history',[])))
        expected={s.casefold() for s in case['expected_titles']}
        ok=bool(expected & {h['title'].casefold() for h in hits})
        passed+=int(ok)
        print(f"{'PASS' if ok else 'REVIEW'}: {case['question']}")
        print('  Retrieved: '+', '.join(h['title'] for h in hits))
    print(f'{passed}/{len(cases)} questions retrieved an expected title in the top results.')
    print('This checks source retrieval only. Review factual answer quality separately.')
    raise SystemExit(0 if passed==len(cases) else 1)

if __name__=='__main__': main()
