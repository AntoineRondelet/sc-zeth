# Benchmarking Gas cost for different MiMC exponents
import zeth.contracts as contracts

from web3 import Web3, HTTPProvider  # type:ignore
w3 = Web3(HTTPProvider("http://localhost:8545"))

# compile MiMC, MerkleeTree contracts
mimc_interface, tree_interface = contracts.compile_util_contracts()

# deploy MimC contract
mimc_instance, mimc_address = contracts.deploy_mimc_contract(mimc_interface)

# deploy MerkleTreeMiMCHash contract
tree_instance = contracts.deploy_tree_contract(tree_interface, 3, mimc_address)

# Test vector generated by using pyClient/zethMimc.py
x = 3703141493535563179657531719960160174296085208671919316200479060314459804651
y = 15683951496311901749339509118960676303290224812129752890706581988986633412003
out = 16797922449555994684063104214233396200599693715764605878168345782964540311877

# Test vectors generated by using pyClient/zethMimc.py
root = 2441541000495724811029127871318798691502895708150678885895101469991191938081
level_1 = 18994625108571498039763404178311223352138299208457461470344693108622989074396
level_2 = 14099405974798296289089207144580827488086367232485193855461335777570080506647


if __name__ == "__main__":

    # MiMC contract unit test
    hash = contracts.mimcHash(
        mimc_instance,
        x.to_bytes(32, byteorder="big"),
        y.to_bytes(32, byteorder="big"),
        b'clearmatics_mt_seed')

    assert int.from_bytes(hash, byteorder="big") == out
    "Hash is NOT correct"

    # MerkleTreeMiMCHash of depth 3 unit test

    # Recover root and merkle tree from the contract
    tree = contracts.getTree(tree_instance)
    recovered_root = contracts.getRoot(tree_instance)

    # Leaves
    for i in range(7, 15):
        assert int.from_bytes(tree[i], byteorder="big") == 0
        "MerkleTree Error Leaves"

    # Level 2
    for i in range(3, 7):
        assert int.from_bytes(tree[i], byteorder="big") == level_2
        "MerkleTree Error Level 2"

    # Level 1
    for i in range(1, 3):
        assert int.from_bytes(tree[i], byteorder="big") == level_1
        "MerkleTree Error Level 1"

    # Root
    assert int.from_bytes(tree[0], byteorder="big") == root
    "MerkleTree Error Root"

    # Recovered root
    assert int.from_bytes(recovered_root, byteorder="big") == root
    "MerkleTree Error Computed Root"

    print("All test passed")
