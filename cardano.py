import json
from typing import List, Tuple
from pycardano import (
    Transaction, 
    TransactionWitnessSet, 
    TransactionBody, 
    VerificationKeyWitness, 
    PaymentSigningKey,
    PaymentVerificationKey, 
    VerificationKey,
    ScriptAll
)

local_private_keys = {
    "local_ssm_cardano_payment": {
        "type": "PaymentSigningKeyShelley_ed25519",
        "description": "PaymentSigningKeyShelley_ed25519",
        "cborHex": "5820995ac5b441ce188c25f1215882cb6974da16508223240c8270f8dd6239559da4",
    },
    "local_ssm_cardano_policy": {
        "type": "PaymentSigningKeyShelley_ed25519",
        "description": "PaymentSigningKeyShelley_ed25519",
        "cborHex": "5820b935aac254d3b02343bd2450a23d05da88485b9fce58df814bf8bfe5a6ebb0fc",
    },
    "local_ssm_cardano_burn": {
        "type": "PaymentSigningKeyShelley_ed25519",
        "description": "PaymentSigningKeyShelley_ed25519",
        "cborHex": "5820d7a3115622150c6714d55ce7295d580683634c293e3d2afc7a6103b54b6a2fa0",
    },
}

class Cardano:
    def __init__(self):
        pass

    # sign a transaciton using a list of signing keys
    def sign_transaction(
        self, tx_body_cbor: str
    ):
        tx_body = TransactionBody.from_cbor(str(tx_body_cbor))
        skey, _ = self.fetch_signer_key(key_name="payment")
        return self.sign_transaction_with_keys(tx_body=tx_body, payment_signing_keys=[skey], native_scripts=None)

    def fetch_signer_key(self, key_name: str) -> Tuple[PaymentSigningKey, VerificationKey]:
        key = f"local_ssm_cardano_{key_name}"
        s_key = local_private_keys.get(key)
        signer_key = PaymentSigningKey.from_json(data=json.dumps(s_key))
        verification_key = PaymentVerificationKey.from_signing_key(key=signer_key) 
        return signer_key, verification_key

    def sign_transaction_with_keys(
        self, tx_body: TransactionBody, payment_signing_keys: List[PaymentSigningKey], native_scripts: List[ScriptAll]
    ) -> Transaction:
        vk_witnesses = []
        for key in payment_signing_keys:
            signature = key.sign(tx_body.hash())
            vk_witnesses.append(VerificationKeyWitness(key.to_verification_key(), signature))

        signed_tx = Transaction(
            tx_body, TransactionWitnessSet(vkey_witnesses=vk_witnesses, native_scripts=native_scripts)
        )
        return signed_tx
    
    