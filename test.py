from flask_jsonrpc.proxy import ServiceProxy
from colorama import Fore, Style, init
from pprint import pprint
from traceback import print_exc

import json, argparse, sys, random, string

# Parse cmdline args
parser = argparse.ArgumentParser()
parser.add_argument("--AddScore", nargs=2, metavar=('NAME', 'SCORE'), help="Add Score to Leaderboard only", dest="AddScore")
parser.add_argument("--GetScores", help="Get leaderboard scores only", action='store_true', dest="GetScores")

args = parser.parse_args()

if args.AddScore:
    try:
        args.AddScore[1] = int(args.AddScore[1])
    except ValueError:
        parser.error("SCORE must be a number")

init() #init colorama

#Initialise JSON-RPC endpoint
server = ServiceProxy('http://127.0.0.1:5000/api')

failed_tests = False

def random_generator(size = 6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for x in range(size))

def test_index():
    print("Performing 'index' API call test.  Ensure's basic API connectivity:")
    try:
        response = server.app.index()
        assert "Welcome" in response['result']
        assert "error" not in response
        print(f'{Fore.GREEN}index test passed{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}index test failed.  Fundamental problem with API server exists.  Exiting...{Style.RESET_ALL}')
        global failed_tests
        failed_tests = True
        print_exc()
    finally:
        if failed_tests == True:
            sys.exit()
        print('Response:', response, '\n')

def test_AddScore(name = 'Morgan', score = 5):
    print("Performing 'AddScore' API call test:")
    response = server.app.AddScore(name, score)
    try:
        assert "Score added" or "Score updated" in response['result']
        assert "Score not updated" not in response['result']
        assert "error" not in response
        print(f'{Fore.GREEN}AddScore test passed{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}AddScore test failed{Style.RESET_ALL}')
        global failed_tests
        failed_tests = True
        print_exc()
    finally:
        print('Response:', response, '\n')

def test_UpdateScore(name = 'Morgan', score = 6):
    print("Performing 'UpdateScore' API call test:")
    response = server.app.AddScore(name, score)
    try:
        assert "Score updated" in response['result']
        assert "error" not in response
        print(f'{Fore.GREEN}UpdateScore test passed{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}UpdateScore test failed{Style.RESET_ALL}')
        global failed_tests
        failed_tests = True
        print_exc()
    finally:
        print('Response:', response, '\n')

def test_AddScoreInvalidData(name = 'Player', score = 'PlayerScore'):
    print("Performing 'AddScore' API call test with invalid data.  Server should error:")
    response = server.app.AddScore(name, score)
    try:
        assert "Score added" not in response
        assert "error" in response
        print(f'{Fore.GREEN}AddScore with invalid data test passed{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}AddScore with invalid data test failed{Style.RESET_ALL}')
        global failed_tests
        failed_tests = True
        print_exc()
    finally:
        print('Response:', response, '\n')

def test_UpdateScoreWithLowerValue(name = 'Morgan', score = '4'):
    print("Performing 'AddScore' API call test with lower 'score' value than existing record. Server should not update the score.:")
    response = server.app.AddScore(name, score)
    try:
        assert "Score not updated." in response['result']
        assert "error" not in response # This should not cause an error as the score is value, just does not warrant an update.
        print(f'{Fore.GREEN}AddScore call with low score value test passed{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}AddScore call with low score value test failed{Style.RESET_ALL}')
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
        assert '6' in str(response['result'])
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
    if args.AddScore:
        test_AddScore(args.AddScore[0], args.AddScore[1])
    elif args.GetScores:
        test_GetScores()
    else:
        random_name = random_generator()
        test_index()
        test_AddScore(name = random_name)
        test_AddScoreInvalidData()
        test_UpdateScore(name = random_name)
        test_UpdateScoreWithLowerValue(name = random_name)
        test_GetScores()
        if failed_tests == False:
            print(f'{Fore.GREEN}ALL TESTS PASSED!{Style.RESET_ALL}')