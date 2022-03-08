from connection import connect
import inquirer


role_dict = {
    "Client": {
        "num": "0",
        "actions": ["Search one or more products", "Exit"],
    },
    "Supplier": {
        "num": "1",
        "actions": [
            "Search one or more products",
            "Add a new product",
            "Transfer the property of a product",
            "Exit",
        ],
    },
    "Transformer": {
        "num": "2",
        "actions": [
            "Search one or more products",
            "Add a new operation",
            "Transfer the property of a product",
            "Exit",
        ],
    },
}


def get_wallet():
    return inquirer.text(
        message="Insert your wallet address",
    )


def main():

    print("Welcome!")

    role = inquirer.list_input(
        message="Specify your role",
        choices=["Client", "Supplier", "Transformer"],
    )

    print(role)
    # web3 = connect(role_dict[role]["num"])

    action = inquirer.list_input(
        message="What action do you want to perform?",
        choices=role_dict[role]["actions"],
    )
    print(action)

    get_wallet()


if __name__ == "__main__":
    main()
