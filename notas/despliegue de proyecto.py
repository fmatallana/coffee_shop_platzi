"""
1, validar que el requirements este con sus versiones especificas
pip freeze para ver las versiones

en las urls gobales se cambia esto

path("/products", include("products.urls")),

por path("", include("products.urls")), y se pone en la parte de arriba ya que django valida cada url, entonces al correr el server y abrir la url lo primero que va a salir es el template de la lista de productos


hacer archivo readme

black permite tener el mismo formateo de codigo en todos los archivos pip install black

black .

pip freeze >
"""
