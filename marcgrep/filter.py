import re

from pymarc import Record


def parse_pattern(pattern):
    parts = pattern.split(",")
    # Convert empty strings to None to support "123,,,,value" use case
    parts = [part if part else None for part in parts]
    # 3.10 Match-Case would be better here
    # We prioritize the field, then the value, then the subfield, and indicators come last
    if len(parts) == 1:
        return parts[0], None, None, None, None
    if len(parts) == 2:
        return parts[0], None, None, None, parts[1]
    if len(parts) == 3:
        return parts[0], None, None, parts[1], parts[2]
    if len(parts) == 4:
        return parts[0], parts[1], None, parts[2], parts[3]
    # combine the rest into the value, convert Nones past the 4th index back to empty string
    value = ",".join([p if p else "" for p in parts[4:]])
    return parts[0], parts[1], parts[2], parts[3], value


class FilterFormatError(Exception):
    pass


class Filter:
    def __init__(self, pattern, inclusive=True) -> None:
        """Pettern is a comma-separated string like
        FIELD,INDICATOR1,INDICATOR2,SUBFIELD,VALUE
        where only FIELD is required and VALUE can itself contain commas
        e.g. 245,cat in the hat -> field:245, value:cat in the hat
        245,4,0,a,cat in the hat -> field:245, ind1:4, ind2:0, subfield:a, value:cat in the hat
        """
        self.inclusive = inclusive
        self.pattern = pattern
        parts = parse_pattern(pattern)
        self.field: str | None = parts[0]
        self.ind1: str | None = parts[1]
        self.ind2: str | None = parts[2]
        self.subfield: str | None = parts[3]
        self.value: str | None = parts[4]
        self.validate()

    def __repr__(self) -> str:
        return f"{'Inclusive' if self.inclusive else 'Exclusive'} Filter: field={self.field}, ind1={self.ind1}, ind2={self.ind2}, subfield={self.subfield}, value={self.value}"

    def validate(self) -> None:
        if not self.field:
            raise FilterFormatError(
                "Field is required; filter pattern cannot be empty."
            )
        if len(self.field) != 3 or not self.field.isdigit():
            raise FilterFormatError(
                f"Field {self.field} is invalid, must be three digits 000-999."
            )
        if self.ind1 is not None and (len(self.ind1) != 1 or not self.ind1.isdigit()):
            raise FilterFormatError(
                f"Indicator 1 {self.ind1} is invalid, must one one digit 0-9."
            )
        if self.ind2 is not None and (len(self.ind2) != 1 or not self.ind2.isdigit()):
            raise FilterFormatError(
                f"Indicator 2 {self.ind2} is invalid, must one one digit 0-9."
            )
        if self.subfield is not None and len(self.subfield) != 1:
            raise FilterFormatError(
                f"Subfield {self.subfield} is invalid, must be one character."
            )

    def match(self, record: Record) -> bool:
        result = self.inclusive
        for field in record.get_fields(self.field):
            # print(re.match(self.value, field.format_field()))
            if self.ind1 and field.indicator1 != self.ind1:
                continue
            if self.ind2 and field.indicator2 != self.ind2:
                continue
            if self.subfield:
                subfields = field.get_subfields(self.subfield)
                if (
                    self.value
                    and not any(
                        re.search(self.value, subfield) for subfield in subfields
                    )
                    or not len(subfields)
                ):
                    continue
            if self.value and not re.search(self.value, field.format_field()):
                continue
            # if we get here, the filter matched
            return result
        return not result
