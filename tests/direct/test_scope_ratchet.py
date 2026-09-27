from conftest import CONTRACT
import json

def llm(vm,pattern,payload): vm.mock_llm(pattern,json.dumps(payload))
def frozen(vm):
 vm.mock_web(r'rules\.example',{'status':200,'body':'0 A cumulative change at or above 10% requires retender.\n1 New scope requires retender.'})
 vm.mock_web(r'award\.example',{'status':200,'body':'Award: maintain the existing north pump array. Value: 100000.'})
def setup(vm,deploy,alice,bob,charlie):
 vm.warp('2035-01-01T00:00:00+00:00');vm.sender=alice;frozen(vm);c=deploy(CONTRACT);c.open_procurement('pump-9','0x'+bob.hex(),'0x'+charlie.hex(),'https://rules.example/materiality','https://award.example/base',100000,1000,600);return c
def measure(vm,impact=400,scope='SAME',indexes=[]):
 code={'SAME':0,'ADJACENT':1,'NEW':2}[scope];mask=sum(1<<v for v in indexes);frozen(vm);vm.mock_web(r'order\.example',{'status':200,'body':'Replace worn seals in the existing north pump array.'});llm(vm,r'.*ScopeRatchet change-order measurement.*',{'impact_bps':impact,'scope_code':code,'trigger_mask':mask})

def test_cumulative_orders_trigger_ratchet(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);direct_vm.sender=direct_bob;measure(direct_vm,600);c.file_change_order('pump-9','https://order.example/one');direct_vm.warp('2035-01-01T00:11:00+00:00');c.finalize_order('pump-9');assert c.get_procurement('pump-9')['cumulative_bps']==600;direct_vm.clear_mocks();direct_vm.sender=direct_bob;measure(direct_vm,450);c.file_change_order('pump-9','https://order.example/two');assert c.get_order('pump-9',2)['requires_retender'] is True
def test_new_scope_requires_retender(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);direct_vm.sender=direct_bob;measure(direct_vm,100,'NEW',[1]);c.file_change_order('pump-9','https://order.example/new');assert c.get_order('pump-9',1)['requires_retender'] is True
def test_only_contractor_files(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);measure(direct_vm)
 with direct_vm.expect_revert('contractor order'): c.file_change_order('pump-9','https://order.example/one')
def test_oversight_can_correct_measurement(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);direct_vm.sender=direct_bob;measure(direct_vm,300);c.file_change_order('pump-9','https://order.example/one');direct_vm.clear_mocks();direct_vm.sender=direct_charlie;measure(direct_vm,1200,'ADJACENT',[0]);direct_vm.mock_web(r'challenge\.example',{'status':200,'body':'The omitted cabling raises the order to twelve percent.'});c.challenge_measurement('pump-9','https://challenge.example/review');assert c.get_order('pump-9',1)['impact_bps']==1200 and c.get_order('pump-9',1)['status']=='CHALLENGED'
def test_validator_rejects_forged_impact(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);measure(direct_vm,400);p=c.procurements['PUMP-9'];result=c._measure(p,'https://order.example/one');assert direct_vm.run_validator(leader_result=result) is True;forged=dict(result);forged['impact_bps']=40;assert direct_vm.run_validator(leader_result=forged) is False
def test_changed_frozen_award_fails(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);direct_vm.clear_mocks();direct_vm.sender=direct_bob;direct_vm.mock_web(r'rules\.example',{'status':200,'body':'0 A cumulative change at or above 10% requires retender.\n1 New scope requires retender.'});direct_vm.mock_web(r'award\.example',{'status':200,'body':'CHANGED AWARD'});direct_vm.mock_web(r'order\.example',{'status':200,'body':'Small repair.'})
 with direct_vm.expect_revert('frozen procurement context changed'): c.file_change_order('pump-9','https://order.example/one')
