import os

from supabase import create_client, Client


class SupabaseException(Exception):
    pass


class SupabaseClient:

    client: Client = None

    def __init__(self):
        self._get_supabase_client()

    def _get_supabase_client(self) -> None:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise SupabaseException(
                "Please set the SUPABASE_URL and SUPABASE_KEY environment variables"
            )
        supabase: Client = create_client(url, key)
        self.client = supabase

    def insert_results_row(
        self,
        level: int,
        total_words: int,
        total_chars: int,
        total_mistakes: int,
        time_taken: float,
        mistakes_dict: dict,
    ) -> None:
        self.client.table("results").insert(
            {
                "level": level,
                "total_words": total_words,
                "total_chars": total_chars,
                "total_mistakes": total_mistakes,
                "time_taken": time_taken,
                "mistakes_by_char": mistakes_dict,
            }
        ).execute()
