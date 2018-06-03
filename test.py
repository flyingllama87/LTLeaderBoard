from flask_jsonrpc.proxy import ServiceProxy
from colorama import Fore, Style, init
import json
from pprint import pprint
from traceback import print_exc
# import click

init()

server = ServiceProxy('http://127.0.0.1:5000/api')

failed_tests = False

def test_index():
    print("Performing 'index' API call test:")
    response = server.app.index()
    try:
        assert "Welcome" in response['result']
        assert "error" not in response
        print(f'{Fore.GREEN}index test passed{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}index test failed{Style.RESET_ALL}')
        global failed_tests
        failed_tests = True
        print_exc()
    finally:
        print('Response:', response, '\n')
    

def test_hello():
    print("Performing 'hello world' API call test:")
    response = server.app.hello('Morgan')
    try:
        assert "Hello, Morgan" in response['result']
        assert "error" not in response
        print(f'{Fore.GREEN}hello world test passed{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}hello world test failed{Style.RESET_ALL}')
        global failed_tests
        failed_tests = True
        print_exc()
    finally:
        print('Response:', response, '\n')

def test_AddScore():
    print("Performing 'AddScore' API call test:")
    response = server.app.AddScore('Morgan', 5)
    try:
        assert "Score added" in response['result']
        assert "error" not in response
        print(f'{Fore.GREEN}AddScore test passed{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}AddScore test failed{Style.RESET_ALL}')
        global failed_tests
        failed_tests = True
        print_exc()
    finally:
        print('Response:', response, '\n')
    

def test_GetScores():
    print("Performing 'Getscores' API call test:")
    response = server.app.GetScores()
    try:
        assert "Morgan" in str(response['result'])
        assert '5' in str(response['result'])
        assert "error" not in str(response['result'])
        score_data = json.loads(response['result'])
        print("Scores:")
        pprint(score_data)
        print(f'{Fore.GREEN}GetScores test passed{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}GetScores test failed{Style.RESET_ALL}')
        global failed_tests
        failed_tests = True
        print_exc()
    finally:
        print('Raw Response:', response, '\n')
    
if __name__ == "__main__":
    test_index()
    test_hello()
    test_AddScore()
    test_GetScores()
    if failed_tests == False:
        print(f'{Fore.GREEN} ALL TESTS PASSED!{Style.RESET_ALL}')