# Task 5: Package demonstration
from attendance import reader, stats, report

if __name__ == '__main__':
    print('Testing attendance package...')
    report.generate_report([['192311001', 'P']])
