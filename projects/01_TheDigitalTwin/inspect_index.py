"""Inspect local index for free; --query makes one billable embedding request."""
import argparse
from rag.vectors import LocalVectors
from rag.chat import retrieval_question


# Print snapshot metadata for free, and optionally run one live semantic query
# so an owner can inspect ranking and retrieved passage text.
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query', help='Question to embed and search (billable)')
    args = parser.parse_args()
    library = LocalVectors()
    print('Format:', library.metadata['format'])
    print('Model:', library.metadata['model_id'])
    print('Shape:', library.vectors.shape)
    print('Built:', library.metadata['created_at'])
    if args.query:
        for hit in library.search(retrieval_question(args.query, [])):
            print(f"\n{hit['score']:.4f} | {hit['source']} | {hit['title']}")
            print(hit['url'] or 'Owner-supplied document')
            print(hit['text'][:650])

if __name__ == '__main__':
    main()
