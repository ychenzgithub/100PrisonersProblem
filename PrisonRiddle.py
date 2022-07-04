import numpy as np
import random

def seq_init(n=100):
    ''' initialize the random sequence
    
    Parameters
    ----------
    n : int
        the number of cards
        
    Returns:
    --------
    seq : list
        sequence of the cards
    seqdone : list
        the flag indicating whether a card has been used for other loops        
    '''
    seq = np.arange(n,dtype='int')
    random.shuffle(seq)
    seqdone = [False]*n
    
    return seq,seqdone

def deri_loop(seq,i_st,seqdone):
    ''' derive a valid loop
    
    Parameters
    ----------
    seq : list
        sequence of the cards
    i_st : int
        the start index of the loop
    seqdone : list
        the flag indicating whether a card has been used for other loops
        
    Returns
    -------
    seqloop : list
        the indices of the derived loop
    seqdone : list
        the updated seqdone list
    '''
    i_next = seq[i_st]
    seqdone[i_st] = True
    seqloop = [i_st]
    while i_next != i_st:
        seqloop.append(i_next)
        seqdone[i_next] = True
        i_next = seq[i_next]        
    return seqloop,seqdone

def deri_allloops(seq,seqdone):
    ''' derive all loops associated with a sequence
    Parameters
    ----------
    seq : list
        sequence of the cards
    seqdone : list
        the flag indicating whether a card has been used for other loops    
    
    Returns
    -------
    alllloops : list
        a dic {loopid : loop element id list} of all loops
    '''
    n = len(seq)
    
    allloops = {}
    loopid = 0
    while sum(seqdone) < n:
        i_st = seqdone.index(False)
        seqloop,seqdone = deri_loop(seq,i_st,seqdone)
        allloops[loopid] = seqloop
        loopid += 1    
    return allloops

def check_result(allloops,n):
    ''' check if the realization indicate a success escape (not a single loop has length > n/2)
    Parameters
    ----------
    alllloops : list
        a dic {loopid : loop element id list} of all loops 
    
    Returns
    -------
    res : bool
        success flag
    '''    
    res = True
    for i, l in allloops.items():
        if len(l) > (n/2):
            res = False
    return res

def one_realization(n=100):
    ''' check one realization
    
    Parameters
    ----------
    n : int
        number of cards
        
    Returns
    -------
    res : bool
        if this realization is a success
    '''    
    # do sequence initialization
    seq,seqdone = seq_init(n=n)
    
    # find all loops
    allloops = deri_allloops(seq,seqdone)
    
    # check if a case of derived allloops represents success (not a single loop has length > n/2)
    res = check_result(allloops,n)

    return res

def n_realizations(nr = 1000, n = 100):
    ''' check multiple realizations and return the fraction of success
    
    Parameters
    ----------
    nr : int
        number of ensemble
    n : int
        number of cards
        
    Returns
    -------
    f_suc : float
        the fraction of success
    '''      
    n_True = 0 
    for ir in range(nr):
        n_True += one_realization(n=n)
        
    f_suc = n_True/nr
    return f_suc

# -----------------------------------------------------------------------------
# Author: Yang Chen (yang.chen@uci.edu)