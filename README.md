# ESPN Fantasy Football Weekly Recapper with GPT-4

This was a little weekend project to build a bot to post a summary of the fantasy football scores for my league each week with GPT-4. It does 3 things:

- Calls the ESPN Fantasy Football API to get the teams/scores for the week
- Passes those to a GPT prompt asking for a funny summary of those scores.
- Posts that to Slack (in this case for our fantasy league Slack channel)

There's also an included Azure Function to allow this to be automated. I have it set up to run every Tuesday morning (official end of the week for Fantasy).

## Here's a sample output from GPT:
```
Ahoy, my fearless fantasy footballers and valiant try-hards! Your self-proclaimed ruler of the realm of stats, points, and tragic lineup decisions – the Commissioner – here to break down the chaotic cacophony that was Week 16 in our league of extraordinary underperformers.

Commence the chest-thumping and the weeping, for we have witnessed the clash of titans and the crumble of cookie-dough teams alike. Let's spread the week's folklore, shall we?

The "almost there but not quite" award goes to Dane Gleesak, who with a valiant 112.4 points managed to still fall short against the ever-so-broken (yet somehow victorious) Weekly injury report, who limped their way to 116.6 points. Prayers go out for the players on IR – may you forever be remembered in Dane's lineup.

Raising the fantasy bar to nosebleed heights, Kuppenheimer, with an astounding 151.4 points, has officially caused Chicken and Wings some serious indigestion this week. Falling shy by less than 10 points at 141.8, Chicken and Wings might consider trading poultry for good luck charms. Better cluck next time!

YEE YEE, oh dear, let's pour out some sports drink for this fallen comrade. With a whopping 78.5 points, you've officially made "Dropping the Ball" the theme song for this week. Meanwhile, Team EGBERT evidently hatched a better plan, scrambling to a moderately respectable 105.0 points.

The all-mighty Ole Diggs Grab brought in a run-of-the-mill 111 points, while Derek Carr, the persona non grata of the week, choked on exhaust fumes at 73.6 points. Josh Jacobs, you've really done it this time, scoring 0.0 points! Are we sure he was playing football and not hide and seek?

Ah, and let's not forget the legendary saga of Fred Smoots party boat, who chaotically sailed to the sullen shores of Defeat, with 82.6 points. Peasants of the South has overthrown their feudal lord this week, seizing a peasant's treasure of 109.6 points.

Team Raymer, the almost-heroes with 91.0 points, looked destiny in the eye and said, "Not today." Conversely, Belichick Yourself, with a rather modest 79.4 points, may need to review their namesake's playbook once or twice more before kickoff.

A blaring fanfare for our highest-scoring ruler of the week, Kupp and his trusty steed Breece Hall, who compiled an earth-shattering 43.1 points themselves. Feel free to strut – just watch out for the low-hanging doorframes.

To Derek Carr, our score-minimalist and apparently misunderstood genius, keep weaving those wondrous tales of strategic bench-warming, your legendary 73.6-point performance will be etched in the annals of "what not to do" for generations to come.

Now, as the dust settles and the waiver wire beckons, remember to lift your chin(s), wipe the tears from your waiver claims, and prepare thy benches. For another week awaits where miracles happen, and so do disasters of epic fantasy proportions.

Stay questionable, my friends.
```


## Installation and Running
- Clone the repo, navigate into the folder
- `pip install .\Function\requirements.txt`
- Add a recapper_settings.txt file at the root of the directory and paste this in. Then change all the {value} items to your values. To get swid and espn_s2, follow this link: https://github.com/cwendt94/espn-api/discussions/150#discussioncomment-133615
  (For the Azure function to run, you'll need to add these key value pairs to your function's app settings.)
  ```
  swid={value}
  espn_s2={value}
  openai_key={value}
  slack_token={value}
  slack_channel_id={value}
  league_id={value}
  ```
- `python local_recapper.py`

