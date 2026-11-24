ZONES = {
 'cooma': dict(name='Cooma', towns=['Cooma','Polo Flat'], prices=('$330','$550','$774'), hot=('$330 (min.)','$495','$697'),
               note='Cooma is our cheapest area — it\'s closest to the Cooma landfill.'),
 'z1': dict(name='Zone 1', towns=['Berridale','Jindabyne','East Jindabyne','Tyrolean Village','Kalkite','Dalgety'], prices=('$440','$660','$884'), hot=('$396','$594','$796'),
               note='Our home patch — we\'re based in Berridale, so these towns get quick deliveries and pickups.'),
 'z2': dict(name='Zone 2', towns=['Crackenback','Moonbah','Numeralla','Nimmitabel','Bredbo','Adaminaby','Anglers Reach','Eucumbene','Bungarby'], prices=('$550','$770','$994'), hot=('$495','$693','$895'),
               note='We run bins out here every week — ask if a truck is already in your area for a sharper price.'),
 'z3': dict(name='Zone 3', towns=['Bombala','Delegate','Bibbenluke','Cathcart','Michelago','Yaouk'], prices=('$660','$880','$1,104'), hot=('$594','$792','$994'),
               note='Further out, but still our patch — give us a call and we\'ll plan deliveries around runs already heading your way.'),
 'alpine': dict(name='Alpine resorts', towns=['Thredbo','Perisher','Smiggin Holes','Guthega','Charlotte Pass','Mount Selwyn'], prices=None, hot=None,
               note='Access can be difficult in some of these areas, so it\'s best to give us a call and walk us through your project\'s access and any special requirements.'),
 'quote': dict(name='Outer areas', towns=['Khancoban','Cabramurra','Kiandra','Countegany','Cann River'], prices=None, hot=None,
               note='Right out to Khancoban, Cabramurra, Countegany and Cann River — call us for a price and we\'ll work out the best way to get a bin to you.'),
}
STATE = {'Cann River':'VIC'}
def slug(t): return t.lower().replace(' ','-')
ALL = [(t,k) for k,z in ZONES.items() for t in z['towns']]
