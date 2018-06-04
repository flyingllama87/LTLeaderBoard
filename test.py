from flask_jsonrpc.proxy import ServiceProxy
from colorama import Fore, Style, init
import json
from pprint import pprint
from traceback import print_exc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--AddScore", nargs=2, metavar="NAME SCORE", help="Add Score to Leaderboard only", dest="score")
# parser.add_argument("Name", type=str, help="Name of player whose score you wish to add")
# parser.add_argument("Score", type=int, help="Score of player whose score you wish to add")

args = parser.parse_args()

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

def test_AddScore(name = 'Morgan', score = 5):
    print("Performing 'AddScore' API call test:")
    response = server.app.AddScore(name, score)
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
    

def test_AddScoreInvalidData(name = 'Player', score = 'PlayerScore'):
    print("Performing 'AddScore' API call test with invalid data:")
    response = server.app.AddScore(name, score)
    try:
        assert "Score added" not in response
        assert "error" in response
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
    if args.score:
        test_AddScore(args.score[0], args.score[1])
    else:
        test_index()
        test_hello()
        test_AddScore()
        test_AddScoreInvalidData()
        test_GetScores()
        if failed_tests == False:
            print(f'{Fore.GREEN} ALL TESTS PASSED!{Style.RESET_ALL}')