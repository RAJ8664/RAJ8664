#!/usr/bin/env python3
"""
Ultimate GitHub Profile Generator - Andrew Grant Style
Generates comprehensive ASCII art profile with all details
"""

import os
import requests
from github import Github, Auth
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import json


def fetch_comprehensive_stats():
    """Fetch comprehensive GitHub statistics"""
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("USERNAME")

    if not token or not username:
        raise ValueError("GITHUB_TOKEN and USERNAME must be set")

    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user(username)

    stats = {
        # Basic Info
        "username": username,
        "name": user.name or username,
        "bio": user.bio or "",
        "company": user.company or "",
        "location": user.location or "",
        "email": user.email or "",
        "blog": user.blog or "",
        "twitter": user.twitter_username or "",
        # GitHub Stats
        "total_stars": 0,
        "total_commits": 0,
        "total_prs": 0,
        "total_issues": 0,
        "total_repos": user.public_repos,
        "followers": user.followers,
        "following": user.following,
        "created_at": user.created_at,
        "contributions_2025": 0,
        "total_forks": 0,
        "total_watchers": 0,
        # Languages
        "languages": defaultdict(int),
        "language_percentages": {},
        # Code Stats
        "total_lines_added": 0,
        "total_lines_deleted": 0,
        "total_lines_of_code": 0,
    }

    print("📦 Fetching repository data...")
    repos = list(user.get_repos())

    for repo in repos:
        stats["total_stars"] += repo.stargazers_count
        stats["total_forks"] += repo.forks_count
        stats["total_watchers"] += repo.watchers_count

        # Languages
        try:
            languages = repo.get_languages()
            for lang, bytes_count in languages.items():
                stats["languages"][lang] += bytes_count
        except:
            pass

        # Commits
        try:
            commits = repo.get_commits(author=user)
            commit_count = min(commits.totalCount, 100)  # Limit to avoid rate limits
            stats["total_commits"] += commit_count

            # Count lines for recent commits
            for i, commit in enumerate(commits[:10]):  # Sample recent commits
                try:
                    stats["total_lines_added"] += commit.stats.additions
                    stats["total_lines_deleted"] += commit.stats.deletions
                except:
                    pass

            if datetime.now(timezone.utc).year == 2025:
                try:
                    commits_2025 = repo.get_commits(
                        author=user, since=datetime(2025, 1, 1, tzinfo=timezone.utc)
                    )
                    stats["contributions_2025"] += min(commits_2025.totalCount, 100)
                except:
                    pass
        except:
            pass

    # Estimate total lines of code
    stats["total_lines_of_code"] = (
        sum(stats["languages"].values()) // 50
    )  # Rough estimate

    # Calculate PRs and Issues
    print("🔀 Fetching PRs and Issues...")
    try:
        query = f"author:{username} type:pr"
        prs = g.search_issues(query)
        stats["total_prs"] = prs.totalCount
    except:
        stats["total_prs"] = 0

    try:
        query = f"author:{username} type:issue"
        issues = g.search_issues(query)
        stats["total_issues"] = issues.totalCount
    except:
        stats["total_issues"] = 0

    # Calculate language percentages
    total_bytes = sum(stats["languages"].values())
    if total_bytes > 0:
        stats["language_percentages"] = {
            lang: (bytes_count / total_bytes) * 100
            for lang, bytes_count in stats["languages"].items()
        }
        stats["language_percentages"] = dict(
            sorted(
                stats["language_percentages"].items(), key=lambda x: x[1], reverse=True
            )
        )

    # Calculate account age
    account_age = datetime.now(timezone.utc) - stats["created_at"]
    stats["account_years"] = account_age.days // 365
    stats["account_months"] = (account_age.days % 365) // 30
    stats["account_days"] = (account_age.days % 365) % 30

    return stats


def generate_andrew_grant_style(stats):
    """Generate Andrew Grant style comprehensive profile"""

    def fmt_num(num):
        """Format large numbers"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.0f}K" if num >= 10000 else f"{num/1000:.1f}K"
        return str(num)

    # Prepare contact info
    contact_lines = []
    if stats["email"]:
        contact_lines.append(
            f"    Email.Personal: ..................... {stats['email']}"
        )
    if stats["blog"]:
        contact_lines.append(
            f"    Email.Work: ......................... {stats['blog']}"
        )
    if stats["location"]:
        contact_lines.append(
            f"    Location: ........................... {stats['location']}"
        )

    # Programming languages (top 10)
    prog_langs = [
        k
        for k in list(stats["language_percentages"].keys())[:10]
        if k
        in [
            "Java",
            "Python",
            "JavaScript",
            "TypeScript",
            "Go",
            "Rust",
            "C",
            "C++",
            "C#",
            "Ruby",
            "PHP",
            "Swift",
            "Kotlin",
            "Scala",
        ]
    ]
    prog_langs_str = (
        ", ".join(prog_langs[:6]) if prog_langs else "Java, Python, JavaScript"
    )

    # Markup languages
    markup_langs = [
        k
        for k in stats["language_percentages"].keys()
        if k in ["HTML", "CSS", "SCSS", "Markdown", "XML", "JSON", "YAML"]
    ]
    markup_langs_str = (
        ", ".join(markup_langs[:6]) if markup_langs else "HTML, CSS, JSON"
    )

    # Calculate lines of code contribution
    lines_added_fmt = fmt_num(stats["total_lines_added"])
    lines_deleted_fmt = fmt_num(stats["total_lines_deleted"])
    total_loc_fmt = fmt_num(stats["total_lines_of_code"])

    # Bio
    bio_line = stats["bio"][:60] + "..." if len(stats["bio"]) > 60 else stats["bio"]

    # Current time
    current_time = datetime.now(timezone.utc).strftime("%B %d, %Y")

    # ASCII art header (smaller, cleaner)
    ascii_art = f"""
```ascii
            @@@@@@@@@@@@@@@@@@
          @@   @@@@@@@@@@@   @@              {stats['username']} ────────────────────────────────
         @@  @@@@@@@@@@@@@@@  @@
        @@  @@@  @@@@@  @@@@@  @@            OS: ........................ Linux, macOS, Windows
       @@  @@@@   @@@   @@@@@@  @@           Uptime: ..................... {stats['account_years']} years, {stats['account_months']} months, {stats['account_days']} days
       @  @@@@@    @    @@@@@@@  @           Host: ....................... GitHub.com
      @  @@@@@@         @@@@@@@@  @          Kernel: ..................... Git
      @  @@@@@@@@     @@@@@@@@@@  @          IDE: ........................ VSCode, IntelliJ IDEA
     @  @@@@@@@@@@@@@@@@@@@@@@@@@  @
     @  @@@@@@@@@@@@@@@@@@@@@@@@@  @         Languages.Programming: ...... {prog_langs_str}
     @  @@@@@@@@@@@@@@@@@@@@@@@@@  @         Languages.Markup: ........... {markup_langs_str}
     @  @@@@@@@@  @@@  @@@@@@@@@  @          Languages.Shell: ............ Bash, PowerShell
      @  @@@@@@   @@@   @@@@@@@  @
      @  @@@@@@@@@@@@@@@@@@@@@  @            Hobbies.Software: ........... Open Source, Web Development
       @  @@@@@@@@@@@@@@@@@@@  @             Hobbies.Hardware: ........... Raspberry Pi, Arduino
       @@  @@@@@@@@@@@@@@@@@  @@             Hobbies.Other: .............. {bio_line if bio_line else 'Coding, Learning'}
        @@  @@@@@@@@@@@@@@@  @@
         @@   @@@@@@@@@@@   @@               Contact
          @@@@@@@@@@@@@@@@@@                 ───────
                                             {chr(10).join(contact_lines) if contact_lines else '    GitHub: ....................... github.com/' + stats['username']}
                                             LinkedIn: ..................... linkedin.com/in/{stats['username'].lower()}
                                             Discord: ...................... {stats['username']}

                                             GitHub Stats
                                             ────────────
                                             Repos: ....... {stats['total_repos']} {('Contributed: ' + str(stats['total_prs'])) if stats['total_prs'] > 0 else ''} | Stars: .......... {stats['total_stars']}
                                             Commits: ..... {fmt_num(stats['total_commits'])} | Followers: ....... {stats['followers']}
                                             Lines of Code on GitHub: {total_loc_fmt} ( +{lines_added_fmt}, -{lines_deleted_fmt} )

                                             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                                             📊 Language Distribution
                                             
{generate_language_bars(stats['language_percentages'])}

                                             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                                             🔥 2025 Activity: {fmt_num(stats['contributions_2025'])} contributions
                                             ⭐ Total Stars Earned: {stats['total_stars']}
                                             🔀 Pull Requests: {stats['total_prs']}
                                             🐛 Issues Created: {stats['total_issues']}
                                             👁️  Watchers: {stats['total_watchers']}

                                             Last Updated: {current_time}
```
"""
    return ascii_art


def generate_language_bars(lang_percentages, max_display=8):
    """Generate language distribution bars"""
    lines = []
    items = list(lang_percentages.items())[:max_display]

    for lang, percentage in items:
        # Create bar
        bar_length = 30
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Format line
        line = f"                                             {lang:<15} {bar} {percentage:>5.1f}%"
        lines.append(line)

    return "\n".join(lines)


def generate_compact_style(stats):
    """Generate a more compact, information-dense style"""

    def fmt(num):
        if num >= 1000:
            return f"{num/1000:.1f}k"
        return str(num)

    # Get top languages
    top_langs = list(stats["language_percentages"].items())[:5]
    lang_str = ", ".join([f"{lang} ({perc:.1f}%)" for lang, perc in top_langs])

    current_time = datetime.now(timezone.utc).strftime("%B %d, %Y")

    ascii_art = f"""
```ascii
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║      ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗                        ║
    ║     ██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗                       ║
    ║     ██║  ███╗██║   ██║   ███████║██║   ██║██████╔╝                       ║
    ║     ██║   ██║██║   ██║   ██╔══██║██║   ██║██╔══██╗                       ║
    ║     ╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝                       ║
    ║      ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝                        ║
    ║                                                                            ║
    ║                          {stats['username']} - {stats['name']:<25}             ║
    ║                                                                            ║
    ╠════════════════════════════════════════════════════════════════════════════╣
    ║                                                                            ║
    ║  💼 PROFILE                                                                ║
    ║  ├─ Location: .................. {stats['location'][:30] if stats['location'] else 'Earth':<30}           ║
    ║  ├─ Email: ..................... {stats['email'][:30] if stats['email'] else 'N/A':<30}           ║
    ║  ├─ Website: ................... {stats['blog'][:30] if stats['blog'] else 'N/A':<30}           ║
    ║  └─ Member Since: .............. {stats['account_years']} years, {stats['account_months']} months ago                ║
    ║                                                                            ║
    ╠════════════════════════════════════════════════════════════════════════════╣
    ║                                                                            ║
    ║  📊 GITHUB STATISTICS                                                      ║
    ║  ├─ Total Repositories: ........ {stats['total_repos']:<6} 📦                                 ║
    ║  ├─ Total Stars Earned: ........ {stats['total_stars']:<6} ⭐                                 ║
    ║  ├─ Total Commits: ............. {fmt(stats['total_commits']):<6} 💻                                 ║
    ║  ├─ Total Pull Requests: ....... {stats['total_prs']:<6} 🔀                                 ║
    ║  ├─ Total Issues: .............. {stats['total_issues']:<6} 🐛                                 ║
    ║  ├─ Total Forks: ............... {stats['total_forks']:<6} 🔱                                 ║
    ║  ├─ Followers: ................. {stats['followers']:<6} 👥                                 ║
    ║  └─ Following: ................. {stats['following']:<6} ➡️                                  ║
    ║                                                                            ║
    ╠════════════════════════════════════════════════════════════════════════════╣
    ║                                                                            ║
    ║  💻 CODE STATISTICS                                                        ║
    ║  ├─ Total Lines of Code: ....... {fmt(stats['total_lines_of_code']):<6} 📝                                 ║
    ║  ├─ Lines Added: ............... +{fmt(stats['total_lines_added']):<5} ✅                                 ║
    ║  ├─ Lines Deleted: ............. -{fmt(stats['total_lines_deleted']):<5} ❌                                 ║
    ║  └─ 2025 Contributions: ........ {fmt(stats['contributions_2025']):<6} 🔥                                 ║
    ║                                                                            ║
    ╠════════════════════════════════════════════════════════════════════════════╣
    ║                                                                            ║
    ║  🌐 TOP LANGUAGES                                                          ║
    ║                                                                            ║
{generate_language_table(stats['language_percentages'])}
    ║                                                                            ║
    ╠════════════════════════════════════════════════════════════════════════════╣
    ║                                                                            ║
    ║  "Talk is cheap. Show me the code." - Linus Torvalds                      ║
    ║                                                                            ║
    ║  Last Updated: {current_time:<56} ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
```
"""
    return ascii_art


def generate_language_table(lang_percentages, max_display=6):
    """Generate language table for compact style"""
    lines = []
    items = list(lang_percentages.items())[:max_display]

    for lang, percentage in items:
        bar_length = 25
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        line = f"    ║  {lang:<15} {bar}  {percentage:>5.1f}%                    ║"
        lines.append(line)

    while len(lines) < 6:
        lines.append(
            "    ║                                                                        ║"
        )

    return "\n".join(lines)


def update_readme(ascii_stats):
    """Update README.md with new stats"""
    readme_path = "README.md"

    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        readme_content = "# My GitHub Profile\n\n"

    start_marker = "<!-- GITHUB_STATS_START -->"
    end_marker = "<!-- GITHUB_STATS_END -->"

    if start_marker in readme_content and end_marker in readme_content:
        before = readme_content.split(start_marker)[0]
        after = readme_content.split(end_marker)[1]
        new_readme = f"{before}{start_marker}\n{ascii_stats}\n{end_marker}{after}"
    else:
        new_readme = (
            f"{readme_content}\n\n{start_marker}\n{ascii_stats}\n{end_marker}\n"
        )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("✅ README.md updated successfully!")


def main():
    """Main function"""
    try:
        print("🚀 Fetching comprehensive GitHub statistics...")
        stats = fetch_comprehensive_stats()

        print(f"\n📊 Stats collected for @{stats['username']}")
        print(f"   - Repos: {stats['total_repos']}")
        print(f"   - Stars: {stats['total_stars']}")
        print(f"   - Commits: {stats['total_commits']}")
        print(f"   - Languages: {len(stats['languages'])}")

        print("\n🎨 Generating comprehensive ASCII profile...")

        # Choose your style:
        ascii_stats = generate_andrew_grant_style(
            stats
        )  # 🎨 Full detailed style like Andrew's
        # ascii_stats = generate_compact_style(stats)      # 📦 Compact information-dense style

        print("📝 Updating README.md...")
        update_readme(ascii_stats)

        print("\n✨ Done! Your comprehensive GitHub profile has been updated.")
        print(f"📈 Total languages detected: {len(stats['languages'])}")
        print(f"💾 Total lines of code: ~{stats['total_lines_of_code']:,}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
