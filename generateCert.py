from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import datetime

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)


subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Organization"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    subject
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).sign(
    private_key, hashes.SHA256(), default_backend()
)

with open("private_key.pem", "wb") as private_key_file:
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_key_file.write(private_key_pem)

with open("cert.pem", "wb") as cert_file:
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    cert_file.write(cert_pem)

print("Certificado e chave privada gerados com sucesso.")
