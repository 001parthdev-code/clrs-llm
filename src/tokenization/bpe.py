from collections import Counter
from corpus import load_corpus
import json



class BPETrainer:

    def __init__(self, vocab_size=8192):
        self.vocab_size = vocab_size

    def build_initial_vocab(self, texts):
        """
        Build the initial vocabulary from individual characters.
        """

        vocab = set()

        for text in texts:
            for char in text:
                vocab.add(char)

        return vocab

    def build_word_frequency(self, texts):
        """
        Count how frequently each word occurs.
        """

        word_counts = Counter()

        for text in texts:
            words = text.split()

            for word in words:
                symbols = tuple(word)
                word_counts[word] += 1

        return word_counts

    def get_pair_counts(self, word_counts):
        """
        Count adjacent symbol pairs weighted by word frequency.
        """

        pair_counts = Counter()

        for symbols, frequency in word_counts.items():

            for i in range(len(symbols) - 1):
                pair = (
                    symbols[i],
                    symbols[i + 1]
                )

                pair_counts[pair] += frequency

        return pair_counts

    def get_best_pair(self, pair_counts):
        """
        Return the most frequent adjacent pair.
        """

        if not pair_counts:
            return None

        return pair_counts.most_common(1)[0][0]

    def merge_pair(self, word_counts, pair):
        """
        Merge one pair everywhere it occurs.
        """

        merged_counts = Counter()

        left, right = pair
        merged = left + right

        for symbols, frequency in word_counts.items():

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

            merged_counts[tuple(new_symbols)] += frequency

        return merged_counts

    def train(self, texts):

        print("Building initial vocabulary...")

        vocabulary = self.build_initial_vocab(texts)

        print(
            f"Initial vocabulary: "
            f"{len(vocabulary)}"
        )

        word_counts = self.build_word_frequency(texts)

        merges = []

        while len(vocabulary) < self.vocab_size:

            pair_counts = self.get_pair_counts(
                word_counts
            )

            best_pair = self.get_best_pair(
                pair_counts
            )

            if best_pair is None:
                break

            merged_token = (
                best_pair[0] +
                best_pair[1]
            )

            if merged_token in vocabulary:
                break

            word_counts = self.merge_pair(
                word_counts,
                best_pair
            )

            vocabulary.add(merged_token)
            merges.append(best_pair)

            if len(merges) % 500 == 0:
                print(
                    f"Vocabulary: "
                    f"{len(vocabulary)} / "
                    f"{self.vocab_size}"
                )

        print(
            f"Training complete. "
            f"Vocabulary size: {len(vocabulary)}"
        )

        return vocabulary, merges




if __name__ == "__main__":

    texts = load_corpus()

    print(f"Loaded sections: {len(texts)}")

    trainer = BPETrainer(vocab_size=8192)

    vocabulary, merges = trainer.train(texts)

    print(f"Final vocabulary: {len(vocabulary)}")
    print(f"Total merges: {len(merges)}")

    output_path = "data/bpe_model.json"

    data = {
        "vocabulary": sorted(vocabulary),
        "merges": [
            list(merge)
            for merge in merges
        ],
        "vocab_size": len(vocabulary),
    }

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"Saved BPE model to {output_path}")