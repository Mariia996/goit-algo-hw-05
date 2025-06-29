class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        """Hash function that uses a built-in function hash()"""
        return hash(key) % self.size

    def insert(self, key, value):
        """Inserts a key-value pair into a hash table."""
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        """Gets the value by key from a hash table."""
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        """Removes a key-value pair from a hash table."""
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for i, pair in enumerate(self.table[key_hash]):
                if pair[0] == key:
                    del self.table[key_hash][i]
                    return True
        return False

H = HashTable(5)
H.insert("car", 5)
H.insert("bus", 10)
H.insert("bicycle", 15)

print(H.get("car"))      # 5
print(H.get("bus"))      # 10
print(H.get("bicycle"))  # 15

H.delete("car")
print(H.get("car"))  # None
