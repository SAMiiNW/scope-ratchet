import json,re
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
ROOT=Path(__file__).parents[1];ENV=ROOT.parents[3]/'accounts.env'
key=re.search(r'^ACCOUNT_1_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',ENV.read_text(),re.M).group(1).strip();owner=create_account(account_private_key=key);client=create_client(chain=studionet,account=owner)
tx=client.deploy_contract(code=(ROOT/'contracts'/'contract.py').read_text(),args=[]);print('deployment_tx='+str(tx),flush=True)
try:r=client.wait_for_transaction_receipt(transaction_hash=tx,wait_until='finalized',retries=180,interval=5000,full_transaction=True)
except TypeError:r=client.wait_for_transaction_receipt(transaction_hash=tx,status='FINALIZED',retries=180,interval=5000,full_transaction=True)
leader=(r.get('consensus_data',{}).get('leader_receipt') or [{}])[0];assert str(r.get('result_name')).upper()=='MAJORITY_AGREE' and str(leader.get('execution_result')).upper()=='SUCCESS';address=(r.get('data') or {}).get('contract_address') or r.get('to_address') or r.get('recipient');print(json.dumps({'contractAddress':address,'deploymentTransaction':str(tx),'wallet':owner.address,'result':r.get('result_name'),'execution':leader.get('execution_result')}))
