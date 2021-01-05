import analyzer

def main():
    config = {
    'image': {
        'resolution': 600
    },
    'tmpdirectory': './tmp'
    }
    analyzer.analyze(config, "X")

main()