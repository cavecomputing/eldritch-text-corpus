# eldritch-text-corpus
> *❝The most merciful thing in the world, I think, is the inability of the human mind to correlate all its contents...❝*   
> — **Howard Phillips Lovecraft**

**Version**: *v0.4*<br>
*291,986~ tokens*<br>
*GOAL: 500,000~ tokens*<br>

---
![image](cthulhu.png)

## Dataset
*This dataset is comprised of two paragraph excerpts from the below stories, novels, and novellas. Please note: these are not complete texts and have had various sections removed or modified that are not conducive to an LLM dataset.*   
| Howard Phillips Lovecraft | Algernon Blackwood |
|-------|-------|
| Call of Cthulhu | The Wendigo |
| Shadow over Innsmouth | The Willows |
| At The Mountains of Madness |
| Cool Air |
| The Colour of Space |
| The Dreams in the Witch House |
| The Dunwich Horror |
| The Festival |
| The Shadow Out of Time |
| The Shunned House |
| The Silver Key |
| The Temple |
| The Thing on the Doorstep |
| The Whisperer in Darkness |

Original GitHub repo located here if you wanna get more personal with the data and scripts I use (make cool things with it!): https://github.com/cavecomputing/eldritch-text-corpus

## Usage

Convert text files to training dataset:

```bash
python scripts/convertDataset.py
```

Options:
- `--texts-dir` - Path to texts directory (default: texts)
- `--authors` - Specific author folders to include (default: all)
- `--output` - Output file name (default: eldritch-text-corpus.jsonl)
- `--min-length` - Minimum character length per paragraph (default: 50)

Example:
```bash
python scripts/convertDataset.py --authors "Howard Phillips Lovecraft" --output my-dataset.jsonl
```
