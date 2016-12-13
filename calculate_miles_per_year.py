import click
import arrow


@click.command()
@click.option('--start', help='Start date to calculate from, in format YYYY-MM-DD')
@click.option('--mileage', help='Current mileage on car')
def calculate(start, mileage):
    start = arrow.get(start)
    duration = arrow.now() - start
    print('Duration in days: {}'.format(duration.days))
    mileage = int(mileage)
    years = duration.days / 365.0
    print('Mileage per year: {:0.2f}'.format(mileage / years))


if __name__ == '__main__':
    calculate()
