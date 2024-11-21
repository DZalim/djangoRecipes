class PlaceholderMixin:
    def add_placeholders(self):
        for field_name, field in self.fields.items():  # ('first_name': field_obj)
            placeholder = field.label or field_name.replace('_', ' ').title()
            field.widget.attrs['placeholder'] = placeholder

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholders()

class LabelMixin:
    def add_labels(self, show_labels=None):
        for field_name, field in self.fields.items():
            if field_name == "image_url":
                field.label = f"{self.get_image_type().title()} Image URL"
            else:
                field.label = field_name.replace("_", " ").title()

            if show_labels:
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' show-label'

class DisabledMixin:
    disabled_fields = []

    def make_fields_disabled(self):
        for field_name in self.disabled_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['disabled'] = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_fields_disabled()