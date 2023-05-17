Experiment to try to replace the Twitter timeline algo with my own that pre-filters my timeline using GPT.

Proof-of-concept works. Looking for help to make it work better.

Components:

1. running process that downloads my timeline every hour and adds it to a mongodb.
2. running process that grades new tweets from #1 based on a GPT query (example topic: "AI research")
3. a script that exports the graded tweets from #2 to a text file into #4 (roadmap: make this a server rather than manual export)
4. a frontend which embeds tweets from #3
