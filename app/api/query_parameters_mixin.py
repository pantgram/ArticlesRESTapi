from rest_framework.exceptions import ValidationError

class QueryParamValidationMixin:
    def get_valid_filters(self):
        """Dynamically fetch allowed filters from the filterset class."""
        valid_filters = set()
        if hasattr(self, "filterset_class"):
             valid_filters.update(self.filterset_class.Meta.fields)
        # Add   other static fielda
        valid_filters.update(['keyword','ordering','limit','offset'])
        return valid_filters

    def get_queryset(self):
        queryset = super().get_queryset()
        valid_filters = self.get_valid_filters()
        query_params = set(self.request.query_params.keys())

        # Check for invalid filters dynamically
        invalid_params = query_params - valid_filters
        if invalid_params:
            raise ValidationError({"error": f"Invalid filter(s): {', '.join(invalid_params)}"})

        return queryset