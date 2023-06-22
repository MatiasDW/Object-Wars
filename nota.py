import subprocess
import re


def run_suite(suite):
    # SELECIONAR LA OPCIÓN PARA VUESTRA PLATAFORMA

    command = ['pytest-3']
    #command = ['pytest']
    #command = ['python3 -m pytest']

    command += ['test.py', '-k', suite]


    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output = stdout.decode('UTF-8')
    
    pos_selected = re.search(r'\bselected\b', output).start()
    pos_slash = output[:pos_selected].rfind("/")
    num_test_total = int(output[pos_slash+1:pos_selected])
    # print(num_test_total)

    pos_deselected = output.rfind('passed')
    pos_slash = [i.start() for i in re.finditer(r",|=",output[:pos_deselected])][-1]
    try:
        num_test_passed = int(output[pos_slash+1:pos_deselected])
    except:
        num_test_passed = 0
    # print(num_test_passed)

    # print("num_test_total:", num_test_total, "num_test_passed:", num_test_passed )
    return num_test_passed/num_test_total


print("""La nota de la actividad se desglosa de la siguiente forma:
    3.5p Tests unitarios
    3.5p Tests de integracion
    2p Tests de funcionalidad
    1p Crear tests
""")
suites = ['Test_unitarios', 'Test_integracion',
          'Test_funcionalidad', 'Test_usuario']
results = [run_suite(suite) for suite in suites]

print(f"""La nota actual de la actividad es:
    {results[0]*3.5}p Tests unitarios
    {results[1]*3.5}p Tests de integracion
    {results[2]*2}p Tests de funcionalidad
    {results[3]}p Crear tests
""")
