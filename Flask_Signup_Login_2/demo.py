from werkzeug.security import generate_password_hash
name = 'salman'
print(generate_password_hash(name, method='pbkdf2:sha256'))