import vlc
import sys
import os
import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box

console = Console()

API_BASE_URL = "https://de1.api.radio-browser.info/json"
current_results = {}
current_station_name = "None"
current_volume = 100

def print_banner():
    banner_text = """
    ██╗    ██╗ █████╗  ██████╗  █████╗ ██████╗ 
    ██║    ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗
    ██║ █╗ ██║███████║██║   ██║███████║██████╔╝
    ██║███╗██║██╔══██║██║▄▄ ██║██╔══██║██╔══██╗
    ╚███╔███╔╝██║  ██║╚██████╔╝██║  ██║██║  ██║
     ╚══╝╚══╝ ╚═╝  ╚═╝ ╚══▀▀═╝ ╚═╝  ╚═╝╚═╝  ╚═╝
          H A S S A N   T E R M I N A L
    """
    banner = Text(banner_text, style="bold green")
    console.print(Align.center(banner))

def display_status():
    status_text = Text()
    status_text.append(f"📡 Now Playing: ", style="bold cyan")
    status_text.append(f"{current_station_name}\n", style="bold white")
    status_text.append(f"🔊 Volume: ", style="bold cyan")
    status_text.append(f"{current_volume}%\n", style="bold green")
    status_text.append(f"🖥️  Operator: ", style="bold cyan")
    status_text.append(f"Waqar Hassan | SECURE", style="bold green")
    
    panel = Panel(status_text, title="[bold magenta]SYSTEM STATUS[/bold magenta]", border_style="cyan", box=box.ROUNDED)
    console.print(panel)

def search_stations(query, search_by="name"):
    with console.status(f"[bold green]Scanning open-source frequencies for '{query}'...", spinner="bouncingBar"):
        try:
            url = f"{API_BASE_URL}/stations/by{search_by}/{query}?limit=15"
            headers = {'User-Agent': 'waqar-radio-cli/1.0'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            stations = response.json()
            
            if not stations:
                console.print(Panel("[bold red]ERROR: No frequencies found. Try a new keyword.[/bold red]", border_style="red"))
                return {}

            table = Table(box=box.MINIMAL_DOUBLE_HEAD, style="cyan")
            table.add_column("ID", justify="center", style="bold magenta")
            table.add_column("Station Target", style="bold green")
            table.add_column("Metadata", style="yellow")
            
            results_dict = {}
            for index, station in enumerate(stations):
                station_id = str(index + 1)
                name = station.get("name", "Unknown").strip()
                url = station.get("url_resolved", "")
                tags = station.get("tags", "")[:40] 
                
                if url: 
                    results_dict[station_id] = {"name": name, "url": url}
                    table.add_row(station_id, name, tags)
                    
            console.print(Panel(table, title=f"[bold yellow]SCAN RESULTS: {query.upper()}[/bold yellow]", border_style="green"))
            return results_dict

        except Exception as e:
            console.print(Panel(f"[bold red]UPLINK FAILED:[/bold red] {e}", border_style="red"))
            return {}

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    global current_results, current_station_name, current_volume
    instance = vlc.Instance("--no-video")
    player = instance.media_player_new()
    
    clear_screen()
    print_banner()
    display_status()
    
    while True:
        console.print("\n[bold yellow]COMMANDS:[/bold yellow] [cyan]search <term>[/cyan] | [cyan]play <id>[/cyan] | [cyan]stop[/cyan] | [cyan]vol <0-100>[/cyan] | [cyan]exit[/cyan]")
        user_input = Prompt.ask("[bold green]waqar@radio:~#[/bold green]").strip().lower().split(maxsplit=1)
        
        if not user_input:
            continue
            
        command = user_input[0]
        
        if command == "search":
            if len(user_input) < 2:
                console.print("[red]Syntax Error: Provide a search term.[/red]")
                continue
            current_results = search_stations(user_input[1])
            
        elif command == "play":
            if len(user_input) < 2:
                console.print("[red]Syntax Error: Provide a Target ID.[/red]")
                continue
                
            station_id = user_input[1]
            station_data = current_results.get(station_id)
            
            if not station_data:
                console.print(f"[red]Error: ID '{station_id}' invalid. Execute search first.[/red]")
                continue
                
            current_station_name = station_data['name']
            clear_screen()
            print_banner()
            display_status()
            
            media = instance.media_new(station_data['url'])
            player.set_media(media)
            player.play()
            
        elif command == "stop":
            current_station_name = "None"
            player.stop()
            clear_screen()
            print_banner()
            display_status()

        elif command == "vol":
            if len(user_input) < 2 or not user_input[1].isdigit():
                console.print("[red]Syntax Error: Specify volume (0-100).[/red]")
                continue
            
            volume = int(user_input[1])
            if 0 <= volume <= 100:
                current_volume = volume
                player.audio_set_volume(volume)
                clear_screen()
                print_banner()
                display_status()
            else:
                console.print("[red]Error: Volume out of bounds.[/red]")
            
        elif command == "exit":
            console.print("[bold red]Terminating session. Goodbye.[/bold red]")
            player.stop()
            sys.exit(0)
            
        else:
            console.print("[red]Command not recognized.[/red]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Session aborted.[/bold red]")
        sys.exit(0)
