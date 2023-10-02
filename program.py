class Program:
    def __init__(self, name, program_url, swag, URL, count, change, is_new, platform, bounty, last_updated):
        self.name = name
        self.program_url = program_url
        self.swag = swag
        self.URL = URL
        self.count = count
        self.change = change
        self.is_new = is_new
        self.platform = platform
        self.bounty = bounty
        self.last_updated = last_updated

    @classmethod
    def from_json(cls, json_data):
        name = json_data.get('name', '')
        program_url = json_data.get('program_url', '')
        swag = json_data.get('swag', False)
        URL = json_data.get('URL', '')
        count = json_data.get('count', 0)
        change = json_data.get('change', 0)
        is_new = json_data.get('is_new', False)
        platform = json_data.get('platform', '')
        bounty = json_data.get('bounty', False)
        last_updated = json_data.get('last_updated', '')

        return cls(name, program_url, swag, URL, count, change, is_new, platform, bounty, last_updated)