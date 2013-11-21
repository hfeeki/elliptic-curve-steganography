# Elliptic Curve Steganography #

### Description
---
A computer program coded in python that allows for secure and covert communication.

Elliptic Curve Steganography allows users to hide a message inside a digital image without noticeably altering the image. 
In addition to the messages being undetectable to the human eye, they are also encrypted for additional security. 

Users can communicate securely and covertly by exchanging images without needing to exchange decryption passwords.

### Protocol for Communication
---
Situation: Alice wants to send a message to Bob.

1. Bob creates a public key image and shares the image with Alice via some predetermined method.
2. Using Bob's public key, Alice creates an encrypted message image and shares it with Bob.
3. Using his public key password, Bob extracts and decrypts the encrypted message from Alice's image.

Note: Public keys can be reused.  Once a public key image has been obtained, one may proceed starting at step 2.


### Python Modules
---
In addition to python, some non-standard modules are necessary to Elliptic Curve Steganography.

The following are the recommended versions that the program has been tested under: 

- Python 2.7: &nbsp;&nbsp; [http://www.python.org/](http://www.python.org/)                                   
- Pillow 2.2.1+: &nbsp;&nbsp; [https://pypi.python.org/pypi/Pillow/](https://pypi.python.org/pypi/Pillow/)        
- PyCrypto 2.6+: &nbsp;&nbsp;  [https://www.dlitz.net/software/pycrypto/](https://www.dlitz.net/software/pycrypto/)
- PySide 1.1.2+: &nbsp;&nbsp;  [https://qt-project.org/wiki/PySide](https://qt-project.org/wiki/PySide)            

If necessary, older versions within reason should work.



### Repository Structure
---
***Top Level Directory***

The top level directory contains the main executable for the program: EllipticCurveSteganography.py.  Use this to run the program. Administrative files, such as the readme and license,  are also in the top level.


***ECS Directory***

The ECS directory contains the technical scripts that do all the cryptography and steganography.  They are called from their respective locations within the GUI.

***GUI Directories***

Contains files related to the graphical user interface (GUI), including scripts and images.
