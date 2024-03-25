from pymarc import Record


def count_records(reader):
    return sum(1 for _ in reader if isinstance(_, Record))
