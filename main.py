from googlesearch import search  # Ensure googlesearch-python is in requirements.txt
import os
import time
from datetime import datetime
import json
import csv
import re
from colorama import Fore, Style, init

init(autoreset=True)

def load_dorks(file_path):
    dorks = {}
    try:
        with open(file_path, "r") as file:
            category = None
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if not line.startswith("site:") and not line.startswith("ext:") and not line.startswith("inurl:"):
                    category = line
                    dorks[category] = []
                elif category:
                    dorks[category].append(line)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Dorks file '{file_path}' not found.")
        exit(1)
    return dorks

def perform_search(query):
    try:
        results = []
        for result in search(query, num_results=10):
            results.append(result)
            time.sleep(2)  # Adding a manual pause to prevent rate-limiting
        return results
    except Exception as e:
        print(f"{Fore.RED}Error performing search: {e}")
        return []

def save_report(report, output_format, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)

    if output_format == "txt":
        with open(filepath, "w") as f:
            for category, links in report.items():
                f.write(f"Category: {category}\n")
                f.writelines(f"{link}\n" for link in links)
    elif output_format == "json":
        with open(filepath, "w") as f:
            json.dump(report, f, indent=4)
    elif output_format == "csv":
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Link"])
            for category, links in report.items():
                for link in links:
                    writer.writerow([category, link])

def replace_domain(query, domain):
    return query.replace("example.com", domain)

def print_banner():
    banner = f"""
{Fore.CYAN}                                                                                  
                                                                                  
                                      ,----..                     ,--.            
,-.----.       ,---,.    ,---,       /   /   \  ,-.----.      ,--/  /| .--.--.    
\    /  \    ,'  .' |  .'  .' `\    /   .     : \    /  \  ,---,': / '/  /    '.  
;   :    \ ,---.'   |,---.'     \  .   /   ;.  \;   :    \ :   : '/ /|  :  /`. /  
|   | .\ : |   |   .'|   |  .`\  |.   ;   /  ` ;|   | .\ : |   '   , ;  |  |--`   
.   : |: | :   :  |-,:   : |  '  |;   |  ; \ ; |.   : |: | '   |  /  |  :  ;_     
|   |  \ : :   |  ;/||   ' '  ;  :|   :  | ; | '|   |  \ : |   ;  ;   \  \    `.  
|   : .  / |   :   .''   | ;  .  |.   |  ' ' ' :|   : .  / :   '   \   `----.   \ 
;   | |  \ |   |  |-,|   | :  |  ''   ;  \; /  |;   | |  \ |   |    '  __ \  \  | 
|   | ;\  \'   :  ;/|'   : | /  ;  \   \  ',  / |   | ;\  \'   : |.  \/  /`--'  / 
:   ' | \.'|   |    \|   | '` ,/    ;   :    /  :   ' | \.'|   | '_\.'--'.     /  
:   : :-'  |   :   .';   :  .'       \   \ .'   :   : :-'  '   : |     `--'---'   
|   |.'    |   | ,'  |   ,.'          `---`     |   |.'    ;   |,'                
`---'      `----'    '---'                      `---'      '---'                  
                                                                                  
{Style.RESET_ALL}                             {Fore.GREEN}Welcome to Redorks v1.0
    """
    print(banner)

def main():
    print_banner()

    dorks_file = "dorks.txt"
    dorks = load_dorks(dorks_file)

    domain = input(f"{Fore.YELLOW}Enter the domain (e.g., example.com): {Style.RESET_ALL}").strip()

    print(f"\n{Fore.BLUE}Categories:{Style.RESET_ALL}")
    for i, category in enumerate(dorks.keys(), 1):
        print(f"{Fore.CYAN}{i}. {category}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}all. Execute all categories{Style.RESET_ALL}")

    choice = input(f"\n{Fore.YELLOW}Enter the category number or 'all': {Style.RESET_ALL}").strip().lower()

    if choice == "all":
        selected_dorks = dorks
    else:
        try:
            choice = int(choice)
            selected_category = list(dorks.keys())[choice - 1]
            selected_dorks = {selected_category: dorks[selected_category]}
        except (ValueError, IndexError):
            print(f"{Fore.RED}Invalid choice. Exiting.{Style.RESET_ALL}")
            return

    output_format = input(f"{Fore.YELLOW}Choose output format (txt/json/csv): {Style.RESET_ALL}").strip().lower()
    if output_format not in ["txt", "json", "csv"]:
        print(f"{Fore.RED}Invalid format. Defaulting to txt.{Style.RESET_ALL}")
        output_format = "txt"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = os.path.join("reports", domain)
    filename = f"dork_report_{timestamp}.{output_format}"

    report = {}

    for category, queries in selected_dorks.items():
        print(f"\n{Fore.MAGENTA}Running dorks for category: {category}{Style.RESET_ALL}")
        results = []
        for query in queries:
            formatted_query = replace_domain(query, domain)
            print(f"{Fore.GREEN}Query: {formatted_query}{Style.RESET_ALL}")
            links = perform_search(formatted_query)
            if links:
                results.extend(links)
        if results:
            report[category] = results

    if report:
        save_report(report, output_format, directory, filename)
        print(f"\n{Fore.GREEN}Recon completed. Report saved to '{os.path.join(directory, filename)}'.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}No results found. No report generated.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
