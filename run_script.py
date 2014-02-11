import OpenPNM

#==============================================================================
'''Build Topological Network'''
#==============================================================================
pn = OpenPNM.Network.Cubic(name='cubic_1').generate(divisions=[35,35,35],lattice_spacing=[0.0001])

#==============================================================================
'''Build Geometry'''
#==============================================================================
geom = OpenPNM.Geometry.Stick_and_Ball(network=pn,name='stick_and_ball',locations=pn.get_pore_indices())
geom.regenerate()

#==============================================================================
'''Build Fluids'''
#==============================================================================
air = OpenPNM.Fluids.Air(network=pn)
air.regenerate()

water = OpenPNM.Fluids.Water(network=pn)
water.regenerate()

#==============================================================================
'''Build Physics Objects'''
#==============================================================================
phys_water = OpenPNM.Physics.GenericPhysics(network=pn,fluid=water,name='standard_water_physics')
phys_water.add_method(prop='capillary_pressure',model='purcell',r_toroid=1e-5)
phys_water.add_method(prop='hydraulic_conductance',model='hagen_poiseuille')
phys_water.add_method(prop='diffusive_conductance',model='bulk_diffusion')
phys_water.regenerate()

phys_air = OpenPNM.Physics.GenericPhysics(network=pn,fluid=air,name='standard_air_physics')
phys_air.add_method(prop='hydraulic_conductance',model='hagen_poiseuille')
phys_air.add_method(prop='diffusive_conductance',model='bulk_diffusion')
phys_air.regenerate()

#==============================================================================
'''Begin Simulations'''
#==============================================================================
'''Perform a Drainage Experiment (OrdinaryPercolation)'''
#------------------------------------------------------------------------------
#Initialize algorithm object
OP_1 = OpenPNM.Algorithms.OrdinaryPercolation(loglevel=20,loggername='OP',name='OP_1',network=pn)
a = pn.get_pore_indices(labels='bottom')
OP_1.run(invading_fluid='water',defending_fluid='air',inlets=a,npts=20)

#b = pn.get_pore_indices(labels='top')
#OP_1.evaluate_trapping(outlets=b)
#OP_1.plot_drainage_curve()

##-----------------------------------------------------------------------------
#'''Perform an Injection Experiment (InvasionPercolation)'''
##-----------------------------------------------------------------------------
##Initialize algorithm object
#IP_1 = OpenPNM.Algorithms.InvasionPercolation(loglevel=10,name='IP_1',network=pn)
#face = pn.get_pore_indices('right',indices=False)
#quarter = sp.rand(pn.get_num_pores(),)<.1
#inlets = pn.get_pore_indices()[face&quarter]
#outlets = pn.get_pore_indices('left')
#IP_1.run(invading_fluid=water,defending_fluid=air,inlets=inlets,outlets=outlets)
#
##-----------------------------------------------------------------------------
#'''Performm a Diffusion Simulation on Partially Filled Network'''
##-----------------------------------------------------------------------------
##Apply desired/necessary pore scale physics methods
#air.regenerate()
#water.regenerate()
#OpenPNM.Physics.multi_phase.update_occupancy_OP(water,Pc=8000)
#OpenPNM.Physics.multi_phase.effective_occupancy(pn,air)
#OpenPNM.Physics.multi_phase.DiffusiveConductance(pn,air)
##Initialize algorithm object
#Fickian_alg = OpenPNM.Algorithms.FickianDiffusion()
##Create boundary condition arrays
#BCtypes = sp.zeros(pn.get_num_pores())
#BCvalues = sp.zeros(pn.get_num_pores())
##Specify Dirichlet-type and assign values
#OP_1.update()
#Fickian_alg = OpenPNM.Algorithms.FickianDiffusion(name='Fickian_alg',network=pn)
#Fickian_alg.set_pore_info(prop='Dirichlet',locations=pn.get_pore_indices(subdomain=['top','bottom']),is_indices=True)
#Dir_pores = sp.zeros_like(pn.get_pore_indices(subdomain='top'))
#Dir_pores[pn.get_pore_indices(subdomain='top')] = 0.8
##Dir_pores[pn.get_pore_indices(subdomain='bottom')] = 0.2
#Fickian_alg.set_pore_data(subdomain='Dirichlet',prop='BCval',data=Dir_pores,indices=pn.get_pore_indices(subdomain=['top']))
##Neumann
##BCtypes[pn.pore_properties['type']==1] = 1
##BCtypes[pn.pore_properties['type']==6] = 4
##BCvalues[pn.pore_properties['type']==1] = 8e-1
##BCvalues[pn.pore_properties['type']==6] = 2e-10
#Fickian_alg.set_boundary_conditions(types=BCtypes,values=BCvalues)
##Run simulation
#Fickian_alg.run(active_fluid=air)
#
#
##Export to VTK
#OpenPNM.Visualization.VTK().write(pn,fluid=water)
