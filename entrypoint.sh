#!/bin/sh -l

gh pr diff >> pr_diff.txt
python main.py pr_diff.txt --output-file pr_body.txt
gh pr edit -F pr_body.txt
