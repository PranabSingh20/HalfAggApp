Replit demo - https://replit.com/@PranabSingh20/Schnorr<br>
Client portal - https://halfaggclient.netlify.app/<br>
Server portal - https://halfaggserver.netlify.app/

A client side user can upload their pdf files which are to be signed. After signing the user will receive a copy of the document with a signature. The cryptography scheme used is schnorr (The curve used is secp256k1). The server can then aggregate all the signatures received followed by individually verifying each signature or collectively aggregate verify all the signatures. The application would make sure that the pdf file was not modified by a third party.
