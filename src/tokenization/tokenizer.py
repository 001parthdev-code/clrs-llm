import json
import re
from pathlib import Path


SPECIAL_TOKENS = {
    "<PAD>": 0,
    "<UNK>": 1,
    "<BOS>": 2,
    "<EOS>": 3,
}


class BPETokenizer:

    def __init__(self):
        self.token_to_id = {}
        self.id_to_token = {}
        self.merges = []
        self.special_tokens = SPECIAL_TOKENS.copy()

    # ---------------------------------------------------------
    # Vocabulary
    # ---------------------------------------------------------

    def build_vocabulary(self, vocabulary, merges):
        """
        Convert the learned BPE vocabulary into integer IDs.
        """

        self.merges = merges

        # Reserve IDs for special tokens.
        self.token_to_id = dict(self.special_tokens)

        next_id = len(self.special_tokens)

        for token in sorted(vocabulary):

            if token not in self.token_to_id:
                self.token_to_id[token] = next_id
                next_id += 1

        self.id_to_token = {
            token_id: token
            for token, token_id in self.token_to_id.items()
        }

    # ---------------------------------------------------------
    # Encoding
    # ---------------------------------------------------------

    def encode_word(self, word):
        """
        Apply learned BPE merges to a single word.
        """

        symbols = list(word)

        for merge in self.merges:

            left, right = merge
            merged = left + right

            new_symbols = []
            i = 0

            while i < len(symbols):

                if (
                    i < len(symbols) - 1
                    and symbols[i] == left
                    and symbols[i + 1] == right
                ):
                    new_symbols.append(merged)
                    i += 2

                else:
                    new_symbols.append(symbols[i])
                    i += 1

            symbols = new_symbols

        return symbols

    def encode(self, text, add_bos=False, add_eos=False):
        """
        Convert text into token IDs.

        Whitespace is preserved instead of using text.split(),
        so the tokenizer does not destroy the original structure.
        """

        tokens = []

        if add_bos:
            tokens.append(
                self.special_tokens["<BOS>"]
            )

        # Split into either whitespace or non-whitespace.
        parts = re.findall(
            r"\S+|\s+",
            text
        )

        for part in parts:

            # -------------------------------------------------
            # Whitespace
            # -------------------------------------------------

            if part.isspace():

                for character in part:

                    token_id = self.token_to_id.get(
                        character,
                        self.special_tokens["<UNK>"]
                    )

                    tokens.append(token_id)

            # -------------------------------------------------
            # Words / punctuation
            # -------------------------------------------------

            else:

                subwords = self.encode_word(part)

                for subword in subwords:

                    token_id = self.token_to_id.get(
                        subword,
                        self.special_tokens["<UNK>"]
                    )

                    tokens.append(token_id)

        if add_eos:
            tokens.append(
                self.special_tokens["<EOS>"]
            )

        return tokens

    # ---------------------------------------------------------
    # Decoding
    # ---------------------------------------------------------

    def decode(self, token_ids):
        """
        Convert token IDs back into text.
        """

        pieces = []

        for token_id in token_ids:

            token = self.id_to_token.get(
                token_id,
                "<UNK>"
            )

            # Do not include special tokens in decoded text.
            if token in self.special_tokens:
                continue

            pieces.append(token)

        return "".join(pieces)

    # ---------------------------------------------------------
    # Saving
    # ---------------------------------------------------------

    def save(self, path):
        """
        Save tokenizer configuration to JSON.
        """

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = {
            "token_to_id": self.token_to_id,

            "merges": [
                list(merge)
                for merge in self.merges
            ],

            "special_tokens": self.special_tokens,
        }

        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    # ---------------------------------------------------------
    # Loading
    # ---------------------------------------------------------

    @classmethod
    def load(cls, path):
        """
        Load tokenizer configuration from JSON.
        """

        path = Path(path)

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        tokenizer = cls()

        tokenizer.token_to_id = {
            token: int(token_id)
            for token, token_id
            in data["token_to_id"].items()
        }

        tokenizer.id_to_token = {
            token_id: token
            for token, token_id
            in tokenizer.token_to_id.items()
        }

        tokenizer.merges = [
            tuple(merge)
            for merge in data["merges"]
        ]

        tokenizer.special_tokens = {
            token: int(token_id)
            for token, token_id
            in data["special_tokens"].items()
        }

        return tokenizer