import os
import requests
from github import Github
from datetime import datetime

ORANGE = "🟠"
ORANGE_DIM = "🔸"


def get_github_stats(username, token):
    """Fetch GitHub statistics"""
    g = Github(token)
    user = g.get_user(username)

    total_repos = user.public_repos
    total_stars = sum([repo.stargazers_count for repo in user.get_repos()])

    # Get contribution data from GitHub GraphQL API
    headers = {"Authorization": f"token {token}"}
    query = f"""
    query {{
      user(login: "{username}") {{
        contributionsCollection {{
          contributionCalendar {{
            totalContributions
            weeks {{
              contributionDays {{
                contributionCount
                date
              }}
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        "https://api.github.com/graphql", json={"query": query}, headers=headers
    )

    total_commits = 0
    contribution_days = []

    if response.status_code == 200:
        data = response.json()
        cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        total_commits = cal["totalContributions"]

        # Get last 7 days of contributions
        for week in cal["weeks"][-2:]:
            for day in week["contributionDays"]:
                contribution_days.append(day["contributionCount"])
        contribution_days = contribution_days[-7:]

    return {
        "repos": total_repos,
        "stars": total_stars,
        "commits": total_commits,
        "followers": user.followers,
        "contributions": contribution_days,
    }


def create_contribution_graph(contributions):
    """Create ASCII contribution graph for last 7 days"""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    graph = (
        "Week   │ Contributions\n───────┼──────────────────────────────────────────\n"
    )

    for i, count in enumerate(contributions[-7:]):
        day = days[i]
        # Create bar with orange squares
        filled = min(count, 10)
        bar = ORANGE * filled + "⬜" * (10 - filled)
        graph += f"{day}    │ {bar} {count}\n"

    return graph


def generate_readme(stats):
    """Generate complete README with ASCII art and stats"""

    contributions_graph = create_contribution_graph(stats["contributions"])
    current_time = datetime.now().strftime("%B %d, %Y at %H:%M:%S UTC")
    
     ascii_art = """
    ⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀
    ⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀
    ⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀
    ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⠟⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠻⣿⣿⣿⣿
    ⣿⣿⣿⡇⠀⣠⣤⣶⣶⣶⣶⣶⣶⣶⣤⣄⠀⠀⢸⣿⣿⣿
    ⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢸⣿⣿⣿
    ⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢸⣿⣿⣿
    ⣿⣿⣿⡇⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⢸⣿⣿⣿
    ⣿⣿⣿⣿⣦⣀⠀⠉⠛⠿⠿⠿⠛⠉⠀⣀⣴⣿⣿⣿⣿⣿
    ⠘⢿⣿⣿⣿⣿⣿⣶⣤⣤⣤⣤⣶⣿⣿⣿⣿⣿⣿⡿⠃
    ⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀
    ⠀⠀⠀⠀⠀⠉⠉⠛⠛⠛⠛⠛⠛⠉⠉⠀⠀⠀⠀⠀⠀
    
    🟠 CODING   🟠 LEARNING
    🟠 BUILDING 🟠 GROWING
    """


    readme_content = f"""<div align="center">
<img src="https://komarev.com/ghpvc/?username=raj8664&label=Profile%20Views&color=ff6600&style=flat" alt="Profile views" />
<img src="https://img.shields.io/github/followers/raj8664?label=Followers&style=flat&color=ff6600" alt="followers" />
<img src="https://img.shields.io/github/stars/raj8664?label=Stars&style=flat&color=ff6600" alt="stars" />
</div>

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Architects+Daughter&color=%23FF6600&size=50&center=true&vCenter=true&height=60&width=600&lines=Heyyy!+I'm+RAJ+ROY+%3C3;RAJ+is+me!!!;Welcome+to+my+profile!" alt="Title"></img>
</div>

## 🟠 ASCII Profile - Auto-Updated Every 6 Hours

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Architects+Daughter&color=%23FF6600&size=50&center=true&vCenter=true&height=60&width=600&lines=Heyyy!+I'm+RAJ+ROY+%3C3;RAJ+is+me!!!;Welcome+to+my+profile!" alt="Title"></img>
</div>

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/People%20with%20professions/Man%20Technologist%20Medium%20Skin%20Tone.png" alt="👨‍💻" width="35" height="35" /> **About Me**

<table align="center">
<tr>
<td width="50%" valign="top">

```
╔═══════════════════════════════════════════════╗
║                                               ║
║  🟠 PROFESSIONAL JOURNEY                      ║
║  ━━━━━━━━━━━━━━━━━━━━━━━                      ║
║                                               ║
║  🎓 B.Tech in CS & Engineering                ║
║     NIT Silchar 🇮🇳                           ║
║                                               ║
║  🧠 Strong in:                                ║
║     • Java, C++, Spring Boot                  ║
║     • React.js, System Design                 ║
║                                               ║
║  🎯 Focus:                                    ║
║     • High-performance applications           ║
║     • Scalable backend systems                ║
║                                               ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  🟠 CURRENTLY EXPLORING                       ║
║  ━━━━━━━━━━━━━━━━━━━━                         ║
║                                               ║
║  ☁️  Cloud Architecture (AWS, Azure)         ║
║  🐳 DevOps & Containerization                ║
║     (Docker, Kubernetes)                      ║
║  🔄 Microservices Architecture                ║
║  🤖 AI/ML Integration                         ║
║                                               ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  🟠 WHEN I'M NOT CODING                       ║
║  ━━━━━━━━━━━━━━━━━━━━                         ║
║                                               ║
║  🎼 Music + Linux Customization               ║
║  🎮 Video Games                               ║
║  🏏 Cricket                                   ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

</td>
<td width="50%" align="center" valign="top">

```
{ascii_art}

```

## 📊 Live GitHub Stats (Updated: {current_time})

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🟠 PUBLIC REPOSITORIES      : {stats['repos']:>4}                      │
│   🟠 TOTAL STARS EARNED       : {stats['stars']:>4}                      │
│   🟠 TOTAL COMMITS (2025)     : {stats['commits']:>4}                      │
│   🟠 FOLLOWERS                : {stats['followers']:>4}                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 🔥 Contribution Activity (Last 7 Days)

```
{contributions_graph}
```

---

## <img src="https://media2.giphy.com/media/QssGEmpkyEOhBCb7e1/giphy.gif?cid=ecf05e47a0n3gi1bfqntqmob8g9aid1oyj2wr3ds3mg700bl&rid=giphy.gif" width="30px" height="25px"> Tech Stack

![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=java&logoColor=white) ![Spring](https://img.shields.io/badge/spring-%236DB33F.svg?style=for-the-badge&logo=spring&logoColor=white) ![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![CPP](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c++&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-%236DB33F.svg?style=for-the-badge&logo=spring&logoColor=white)

![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)

![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![CSS](https://img.shields.io/badge/css-%23F05033.svg?style=for-the-badge&logo=css&logoColor=white) ![TypeScript](https://img.shields.io/badge/typescript-%23563D7C.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Angular](https://img.shields.io/badge/angular-%23563D7C.svg?style=for-the-badge&logo=angular&logoColor=white)

## 📈 GitHub Statistics

<div align="center">
  <a href="https://github.com/RAJ8664">
    <div style="display: flex; justify-content: space-between; width: 100%; flex-wrap: wrap; gap: 0px;">
    <img src="https://github-readme-stats.vercel.app/api?username=RAJ8664&hide_border=true&border_radius=15&show_icons=true&theme=dark&title_color=ff6600&icon_color=ff6600&text_color=ffffff&bg_color=0d1117" alt="Raj's GitHub stats" style="width: 40%; height: 88%;">
    <img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=RAJ8664&theme=dark&hide_border=true" alt="Raj's GitHub profile details" style="width: 55%; height: 92%;">
</div>
  <br>
    <div align="center">
        <table>
        <tr>
            <td>
            <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=RAJ8664&hide=html&hide_border=true&layout=compact&langs_count=8&theme=dark&title_color=ff6600&text_color=ffffff&bg_color=0d1117" alt="Top Languages">
            </td>
            <td>
            <img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=RAJ8664&theme=dark&hide_border=true" alt="Repos Per Language">
            </td>
            <td>
            <img src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=RAJ8664&theme=dark&hide_border=true" alt="Most Commit Language">
            </td>
        </tr>
        </table>
    </div>
  </a>
</div>

[![trophy](https://github-profile-trophy.vercel.app/?username=RAJ8664&theme=darkhub&no-frame=true&margin-w=10&column=8&rank=-?,-Unknown&title_color=ff6600)](https://github.com/ryo-ma/github-profile-trophy)

## 🏆 Featured Contributions

<table>
<tr>
<td width="50%">
<div align="center">
  <a href="https://github.com/arthurr455565/BookWeb">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username=arthurr455565&repo=BookWeb&theme=dark&bg_color=0d1117&title_color=ff6600&text_color=c9d1d9&icon_color=ff6600&border_color=30363d&hide_border=false&show_icons=true" alt="BookWeb" />
  </a>
</div>
<p align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=orange" alt="React" />
  <img src="https://img.shields.io/badge/Node.js-43853D?style=flat-square&logo=node.js&logoColor=orange" alt="Node.js" />
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=flat-square&logo=mongodb&logoColor=orange" alt="MongoDB" />
</p>
</td>
<td width="50%">
<div align="center">
  <a href="https://github.com/cpinitiative/usaco-guide">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username=cpinitiative&repo=usaco-guide&theme=dark&bg_color=0d1117&title_color=ff6600&text_color=c9d1d9&icon_color=ff6600&border_color=30363d&hide_border=false&show_icons=true" alt="USACO Guide" />
  </a>
</div>
<p align="center">
  <img src="https://img.shields.io/badge/MDX-1B1F24?style=flat-square&logo=markdown&logoColor=orange" alt="MDX" />
  <img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=orange" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=orange" alt="TypeScript" />
</p>
</td>
</tr>
<tr>
<td width="50%">
<div align="center">
  <a href="https://github.com/ComputerScienceSoceityNITS/css-official-website-2025-26">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username=ComputerScienceSoceityNITS&repo=css-official-website-2025-26&theme=dark&bg_color=0d1117&title_color=ff6600&text_color=c9d1d9&icon_color=ff6600&border_color=30363d&hide_border=false&show_icons=true" alt="CSS Website" />
  </a>
</div>
<p align="center">
  <img src="https://img.shields.io/badge/JavaScript-323330?style=flat-square&logo=javascript&logoColor=orange" alt="JavaScript" />
  <img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=orange" alt="React" />
</p>
</td>
<td width="50%">
<div align="center">
  <a href="https://github.com/raj8664/intern">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username=raj8664&repo=intern&theme=dark&bg_color=0d1117&title_color=ff6600&text_color=c9d1d9&icon_color=ff6600&border_color=30363d&hide_border=false&show_icons=true" alt="Intern" />
  </a>
</div>
<p align="center">
  <img src="https://img.shields.io/badge/JavaScript-323330?style=flat-square&logo=javascript&logoColor=orange" alt="JavaScript" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=orange" alt="PostgreSQL" />
</p>
</td>
</tr>
</table>

---

## 👋 Connect With Me

<div align="center">

[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/royraj20/)&nbsp;
[![LeetCode](https://img.shields.io/badge/LeetCode-FFA116.svg?style=for-the-badge&logo=LeetCode&logoColor=white)](https://leetcode.com/u/RkRoy/)&nbsp;
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?style=for-the-badge&logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100033828349789)&nbsp;
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rajr86642@gmail.com)&nbsp;
[![Codeforces](https://img.shields.io/badge/codeforces-1F8ACB.svg?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/CipherSphinx_Raj)

</div>

---

<div align="center">
<sub>🤖 This profile is auto-updated every 6 hours via GitHub Actions | Last updated: {current_time}</sub>
</div>
"""

    return readme_content


if __name__ == "__main__":
    username = os.environ.get("USERNAME", "raj8664")
    token = os.environ.get("GITHUB_TOKEN")

    if not token:
        print("❌ GITHUB_TOKEN not found!")
        exit(1)

    print("🔍 Fetching GitHub stats...")
    stats = get_github_stats(username, token)

    print("📝 Generating README...")
    readme_content = generate_readme(stats)

    print("💾 Writing to README.md...")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("✅ README.md updated successfully!")
    print(f"   Repos: {stats['repos']}")
    print(f"   Stars: {stats['stars']}")
    print(f"   Commits: {stats['commits']}")
    print(f"   Followers: {stats['followers']}")
