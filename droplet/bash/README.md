### Bash scripts for droplet project

Several bash scripts used to automate job submission and analysis.

parallel.sh submits several jobs at once using qsub, differing by a single integer command line argument which runs over a specified range. e.g., run job1, job2, ..., job7.

subAll.sh, parseAll.sh, and makeMovies.sh use parallel.sh to call analyze.sh, parse_centered.sh, and movie.sh for several cases at once.
