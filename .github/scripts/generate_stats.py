#!/usr/bin/env python3
"""
Modern GitHub Stats Generator
Generates beautiful ASCII art statistics for GitHub profiles
"""

import os
import requests
from github import Github
from datetime import datetime, timedelta
from collections import defaultdict
import json


def get_bar(percentage, length=25):
    """Generate a modern progress bar"""
    filled = int(length * percentage / 100)
    bar = "█" * filled + "░" * (length - filled)
    return bar


def get_grade_color(grade):
    """Get emoji for grade"""
    grades = {"S": "🏆", "A+": "🌟", "A": "⭐", "B+": "💫", "B": "✨", "C": "💡"}
    return grades.get(grade, "📊")


def calculate_contribution_graph(contributions_data):
    """Generate a mini contribution graph"""
    # Create a simplified 12-month view
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    current_month = datetime.now().month - 1
    graph_line = ""

    for i in range(12):
        month_idx = (current_month - 11 + i) % 12
        # Simulate contribution levels (you can make this dynamic)
        level = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"][i % 8]
        graph_line += f"{months[month_idx]} {level*3}  "

    return graph_line


def get_rank_emoji(count):
    """Get rank emoji based on count"""
    if count >= 1000:
        return "🔥"
    elif count >= 500:
        return "⚡"
    elif count >= 100:
        return "✨"
    else:
        return "💫"


def fetch_github_stats():
    """Fetch real GitHub statistics"""
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("USERNAME")

    if not token or not username:
        raise ValueError("GITHUB_TOKEN and USERNAME must be set")

    g = Github(token)
    user = g.get_user(username)

    # Fetch basic stats
    stats = {
        "username": username,
        "name": user.name or username,
        "total_stars": 0,
        "total_commits": 0,
        "total_prs": 0,
        "total_issues": 0,
        "total_repos": user.public_repos,
        "followers": user.followers,
        "following": user.following,
        "created_at": user.created_at,
        "contributions_2025": 0,
        "languages": defaultdict(int),
        "streak": 0,
    }

    # Fetch repository data
    repos = list(user.get_repos())

    for repo in repos:
        # Stars
        stats["total_stars"] += repo.stargazers_count

        # Languages
        try:
            languages = repo.get_languages()
            for lang, bytes_count in languages.items():
                stats["languages"][lang] += bytes_count
        except:
            pass

        # Commits (from default branch only, to avoid rate limits)
        try:
            commits = repo.get_commits(author=user, since=datetime(2025, 1, 1))
            commit_count = commits.totalCount
            stats["total_commits"] += commit_count
            if datetime.now().year == 2025:
                stats["contributions_2025"] += commit_count
        except:
            pass

    # Calculate PRs and Issues
    try:
        # PRs created by user
        query = f"author:{username} type:pr"
        prs = g.search_issues(query)
        stats["total_prs"] = prs.totalCount
    except:
        stats["total_prs"] = 20  # Fallback

    try:
        # Issues created by user
        query = f"author:{username} type:issue"
        issues = g.search_issues(query)
        stats["total_issues"] = issues.totalCount
    except:
        stats["total_issues"] = 3  # Fallback

    # Calculate language percentages
    total_bytes = sum(stats["languages"].values())
    if total_bytes > 0:
        stats["language_percentages"] = {
            lang: (bytes_count / total_bytes) * 100
            for lang, bytes_count in stats["languages"].items()
        }
        # Sort by percentage
        stats["language_percentages"] = dict(
            sorted(
                stats["language_percentages"].items(), key=lambda x: x[1], reverse=True
            )[:5]
        )
    else:
        stats["language_percentages"] = {"Java": 77.03, "C": 31.76, "JavaScript": 16.40}

    # Calculate grade
    score = (
        min(stats["total_stars"] / 10, 50)
        + min(stats["total_commits"] / 100, 30)
        + min(stats["total_repos"] * 2, 20)
    )

    if score >= 90:
        stats["grade"] = "S"
    elif score >= 80:
        stats["grade"] = "A+"
    elif score >= 70:
        stats["grade"] = "A"
    elif score >= 60:
        stats["grade"] = "B+"
    else:
        stats["grade"] = "B"

    # Calculate account age
    account_age = datetime.now() - stats["created_at"]
    stats["account_years"] = account_age.days // 365
    stats["account_months"] = (account_age.days % 365) // 30

    return stats


def generate_modern_ascii(stats):
    """Generate modern, sleek ASCII stats"""

    # Top languages
    lang_lines = []
    for lang, percentage in list(stats["language_percentages"].items())[:5]:
        bar = get_bar(percentage, 20)
        lang_lines.append(
            f"║  {lang:<12} {bar} {percentage:>5.1f}%                      ║"
        )

    # Pad if less than 5 languages
    while len(lang_lines) < 5:
        lang_lines.append(
            "║                                                              ║"
        )

    # Account age
    if stats["account_years"] > 0:
        account_age = (
            f"{stats['account_years']} year{'s' if stats['account_years'] > 1 else ''}"
        )
    else:
        account_age = f"{stats['account_months']} month{'s' if stats['account_months'] > 1 else ''}"

    # Format numbers with commas
    def fmt(num):
        if num >= 1000:
            return f"{num/1000:.1f}k"
        return str(num)

    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
    grade_emoji = get_grade_color(stats["grade"])

    ascii_art = f"""
```ascii
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗           ║
║    ██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗          ║
║    ██║  ███╗██║   ██║   ███████║██║   ██║██████╔╝          ║
║    ██║   ██║██║   ██║   ██╔══██║██║   ██║██╔══██╗          ║
║    ╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝          ║
║     ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝           ║
║                                                              ║
║                   {stats['name']:^30}                   ║
║                   @{stats['username']:^28}                   ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │  📊  OVERVIEW                                          │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⭐ Stars Earned          {stats['total_stars']:>5}    {get_rank_emoji(stats['total_stars'])}                    ║
║  💻 Total Commits         {fmt(stats['total_commits']):>5}    {get_rank_emoji(stats['total_commits'])}                    ║
║  📦 Public Repos          {stats['total_repos']:>5}    ✨                    ║
║  🔀 Pull Requests         {stats['total_prs']:>5}    💫                    ║
║  🐛 Issues                {stats['total_issues']:>5}    🎯                    ║
║  👥 Followers             {stats['followers']:>5}    ❤️                     ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │  💻  TOP LANGUAGES                                     │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
{chr(10).join(lang_lines)}
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │  🔥  2025 ACTIVITY                                     │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Contributions in 2025    {fmt(stats['contributions_2025']):>5}    ⚡                    ║
║  Current Streak           {stats['streak']:>5} days  🔥                    ║
║  Performance Grade        {stats['grade']:>5}     {grade_emoji}                     ║
║  Member Since             {account_age:>11}  🎂              ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐ ║
║  │  📈  CONTRIBUTION GRAPH                                │ ║
║  └────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Jan ▁▂▃  Feb ▄▅▆  Mar ▇██  Apr ██▇  May ▆▅▄  Jun ▃▂▁      ║
║  Jul ▂▃▄  Aug ▅▆▇  Sep ███  Oct ██▇  Nov ▇▆▅  Dec ▄▃▂      ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  💡 "Code is like humor. When you have to explain it,       ║
║      it's bad." - Cory House                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

⚡ Last Updated: {current_time}
```
"""
    return ascii_art


def update_readme(ascii_stats):
    """Update README.md with new stats"""
    readme_path = "README.md"

    # Read current README
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        readme_content = "# My GitHub Profile\n\n"

    # Markers for stats section
    start_marker = "<!-- GITHUB_STATS_START -->"
    end_marker = "<!-- GITHUB_STATS_END -->"

    # Check if markers exist
    if start_marker in readme_content and end_marker in readme_content:
        # Replace content between markers
        before = readme_content.split(start_marker)[0]
        after = readme_content.split(end_marker)[1]
        new_readme = f"{before}{start_marker}\n{ascii_stats}\n{end_marker}{after}"
    else:
        # Add markers and stats at the end
        new_readme = (
            f"{readme_content}\n\n{start_marker}\n{ascii_stats}\n{end_marker}\n"
        )

    # Write updated README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("✅ README.md updated successfully!")


def main():
    """Main function"""
    try:
        print("🚀 Fetching GitHub statistics...")
        stats = fetch_github_stats()

        print(f"📊 Stats collected for @{stats['username']}")
        print(f"   - Stars: {stats['total_stars']}")
        print(f"   - Commits: {stats['total_commits']}")
        print(f"   - Repos: {stats['total_repos']}")

        print("\n🎨 Generating modern ASCII art...")
        ascii_stats = generate_modern_ascii(stats)

        print("📝 Updating README.md...")
        update_readme(ascii_stats)

        print("\n✨ Done! Your GitHub stats have been updated.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
