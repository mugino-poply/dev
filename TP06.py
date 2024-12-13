import argparse
import subprocess
import re

def parse_traceroute(output):
    ip_pattern = re.compile(r'\(([\d.]+)\)')
    ips = ip_pattern.findall(output)
    return ips

def traceroute(target, progressive=False):
    command = ["traceroute", target]
    ips = []

    if progressive:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            with process.stdout:
                for line in iter(process.stdout.readline, ''):
                    print(line.strip())
                    ips.extend(parse_traceroute(line))
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
    else:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ips = parse_traceroute(result.stdout)

    return ips

def save_to_file(ips, filename):
    with open(filename, 'w') as f:
        for ip in ips:
            f.write(ip + '\n')

def main():
    parser = argparse.ArgumentParser(description="script traceroute")
    parser.add_argument("target", help="URL ou adresse IP à tracer")
    parser.add_argument("-p", "--progressive", action="store_true", help="Afficher les résultats progressivement")
    parser.add_argument("-o", "--output-file", help="Fichier d'output pour sauvegarder les résultats")

    args = parser.parse_args()

    ips = traceroute(args.target, args.progressive)

    if not args.progressive:
        for ip in ips:
            print(ip)

    if args.output_file:
        save_to_file(ips, args.output_file)

if __name__ == "__main__":
    main()
