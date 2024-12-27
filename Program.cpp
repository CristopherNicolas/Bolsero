#include <iostream>
#include <cstdlib> // Para usar system()

using namespace std;

int main() {
    // Nombre del script Python que deseas ejecutar
    string pythonScript = "Engine.py";

    // Comando para ejecutar el script Python
    string command = "python " + pythonScript;

        
        cout<<"Se está buscando y guardando info de la bolsa de santiago..."<<endl;
    // Ejecuta el script Python
    int result = system(command.c_str());

    // Verifica si hubo algún error
    if (result == 0) {
        cout << "El script Python se ejecutó correctamente." << endl;
    } else {
        cout << "Ocurrió un error al ejecutar el script Python." << endl;
    }

    return 0;
}
