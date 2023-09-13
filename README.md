# Implementation-of-RSA
An Iterative secure banking system consisting of a bank server and multiple clients

Each bank user can transfer money to another user. The bank server maintains a file “passwd” that stores users’ ID and hashed passwords. Passwords are hashed using SHA1 or MD5.
The bank server maintains a file “balance”, which stores the balance of the account of each user

1: The client connects to the bank server.

2: The client prompts the user to enter his/her ID and password.

3: The client generates a symmetric key K, sends E(Kpub, K) and E(K, ID||password) to the bank server, where id and password are the user’s ID and password entered, respectively.

4: The bank decrypts the E(Kpub, K) using Kprb and gets the symmetric key K. The bank then decrypts E(K, ID||password) using K and gets the ID and the password. Next, the bank computes the hash of the password and compares it against the hash stored in file “passwd”. If the ID and the password are correct, then the bank sends 1 to the client; otherwise 

5: If the password is incorrect, the client prompts the user to enter the id and password again.

6: The user can also transfer money and is prompted to enter the ID to which the money is transferred, and the amount of money transferred. The client then sends them to the server. If there is enough money in the user’s account, then the server updates the “balance” file.
