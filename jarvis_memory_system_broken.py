#!/usr/bin/env python3
"""
JARVIS Memory System - Advanced Memory Management and Learning
Persistent memory, conversation history, and knowledge base for JARVIS Supreme Being AI
"""

import json
import os
import sqlite3
import hashlib
import pickle
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import threading
from collections import defaultdict

class JarvisMemorySystem:
    """Advanced memory management system for JARVIS Supreme Being AI"""
    
    def __init__(self, memory_dir: str = "supreme_memory"):
        self.memory_dir = memory_dir
        self.db_path = os.path.join(memory_dir, "jarvis_memory.db")
        self.knowledge_path = os.path.join(memory_dir, "knowledge_base.json")
        self.conversations_path = os.path.join(memory_dir, "conversations.json")
        self.preferences_path = os.path.join(memory_dir, "user_preferences.json")
        self.skills_path = os.path.join(memory_dir, "learned_skills.json")
        
        # Memory categories
        self.memory_types = {
            'short_term': [],      # Current session memory
            'long_term': {},       # Persistent memory
            'episodic': [],        # Conversation episodes
            'semantic': {},        # Knowledge and facts
            'procedural': {},      # Skills and procedures
            'working': {}          # Active processing memory
        }
        
        # Memory statistics
        self.memory_stats = {
            'total_conversations': 0,
            'total_interactions': 0,
            'knowledge_entries': 0,
            'learned_skills': 0,
            'memory_size_mb': 0,
            'last_cleanup': None
        }
        
        # Thread lock for concurrent access
        self.memory_lock = threading.Lock()
        
        # Initialize memory system
        self.initialize_memory_system()
    
    def initialize_memory_system(self):
        """Initialize the memory system and database"""
        print("🧠 INITIALIZING JARVIS MEMORY SYSTEM...")
        
        try:
            # Create memory directory
            os.makedirs(self.memory_dir, exist_ok=True)
            
            # Initialize SQLite database
            self.init_database()
            
            # Load existing memory
            self.load_memory()
            
            # Update statistics
            self.update_memory_stats()
            
            print("✅ JARVIS Memory System initialized successfully")
            print(f"📊 Memory Statistics: {self.memory_stats}")
            
        except Exception as e:
            print(f"❌ Memory system initialization error: {e}")
    
    def init_database(self):
        """Initialize SQLite database for memory storage"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TEXT,
                    user_input TEXT,
                    jarvis_response TEXT,
                    context TEXT,
                    sentiment REAL,
                    importance INTEGER,
                    tags TEXT
                )
            ''')
            
            # Knowledge base table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    content TEXT,
                    source TEXT,
                    confidence REAL,
                    timestamp TEXT,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TEXT
                )
            ''')
            
            # User preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    preference_type TEXT,
                 xecute('''
   cursor.e    
         stson exiassociatiheck if      # C       
                    ursor()
 = conn.c    cursor      :
      ath) as connf.db_pt(sel.connecte3sqli    with         
         ()
   ).isoformate.now(im= datetmestamp   ti
              try:   ""
 "associatione concept """Stor:
        h: float) strengt: str,pt_bnce, cocept_a: stron, cciation(selfsso def store_a
   0.1)
    _b, rd_a, wordociation(wotore_ass.s        self       
     ort words # Filter sh > 3: en(word_b) 3 and lword_a) > len(    if           :3]:
 response[words_r word_b in   fo   s
       sociation too many ast to avoidmi # Li:3]: ords_input[in w for word_a   pts
     onced response cnput anns between iiatioocte assCrea # 
       )
        ).split(se.lower(spon = jarvis_reonsespwords_re      
  )er().split(ut.lowser_inp= us_input rdwo        nced)
nhang (can be en learniatioe associimpl      # Ss"""
  ationsocie concept as"Updat       ""
 ponse: str):esarvis_r: str, j, user_inputons(selfte_associatiupda  
    def s
  erencepref    return     
            })
       r_input
 lue': use 'va         s',
      ype': 'like        't   
     es.append({  preferenc         r():
 .loweut user_inp" in   if "like      
       })
            t
inpuuser_': value     '    ,
       ce'al_preferen 'gener   'type':           ppend({
  ces.aferen pre        ():
   input.lower" in user_refer   if "pction
     rence detee prefeimpl   # S     
      []
   ences =refer   p   ut"""
  inprences from t user prefe"""Extrac        ict]:
ist[D -> L: str) user_inputf,selnces(_prefere extract 
    defems
   knowledge_it  return      
        
        })6
     : 0.fidence'   'con            r_input,
  usecontent':         'n',
       se 'unknow() el_input.splitif userplit()[0] t.ser_inpuc': uspi        'to        {
tems.append(ge_i    knowlednt
        emet statl faciaotent     # P:
       input user_ not in?"wer() and "_input.loin user if "is"        ith NLP)
ced wan be enhanfor facts (cing ttern matchSimple pa
        # []
        ms = e_iteowledg       kn
 ction""" from interaknowledgeial otentact p""Extr   "t]:
     t[Dicstr) -> Lisnse: poresarvis_put: str, juser_in, dge(selfct_knowleextra
    def  rds
   ywo   return ke
           
  pend(term)words.apey   k            n text:
  i   if term      rms:
   ch_teterm in te for    
       er()
     .lowse)_responrvis+ ja " " user_input +  text = (         
']
     databasee', 'api', 'ariablon', 'v', 'functirithm', 'algo'data               g', 
      learninine  'mach', 'ai','programming',  'codeavascript',on', 'j = ['pythh_terms     tecs
   ermal ttechnicommon 
        # C      []
   s =     keyword
   with NLP)enhanced ion (can be  extractkeyword  # Simple ""
      nversation"om co frtract tags""Ex   "  
   ist[str]:tr) -> Lse: sspon jarvis_re_input: str, usergs(self,xtract_taef e
    dt)
    gative_counount + neve_c/ (positicount)  - negative_ve_counturn (positi   ret    
     rn 0.0
           retu     = 0:
 =ative_countegunt + ne_coositiv      if p   
  
     t_lower)ex ts if word inegative_word in nword sum(1 for nt =ou negative_cr)
       owein text_lf word e_words iositiv in por wordnt = sum(1 fe_cousitiv    poower()
     = text.lt_lower  tex  
      
      'worst']ble', ike', 'horri', 'dislte'haul', , 'awfterrible'['bad', '_words =  negative]
       , 'like'ic', 'love'l', 'fantast', 'wonderfut', 'amazing 'excellenat',', 'greoods = ['gsitive_word     po"""
   ith ML)hanced w(can be ens ysi analent sentim"""Simple      
   -> float:tr)ext: sent(self, tlyze_sentim    def ana   

 t()[:16]).hexdigesode())}".enc_{os.getpid(at()}ow().isoformtime.nateb.md5(f"{dhashli   return "
     "ion ID"nique sessate u"""Gener
        > str:f) -sion_id(selerate_sesdef gens
    odHelper meth  # 
    
  turn False        re   : {e}")
 memoryimporting  Error "❌(f       print
     ion as e:ceptept Ex      exc    
          rn True
  retu          
_path}"){importom:  imported frory✅ Mem"rint(f           p     
       alue)
  pref_vref_type,ference(p.store_pre     self  
         ():items}).', {preferences_data.get('importin pref_value pe, pref_ty       for s
     ence preferport      # Im   
      
             )            e', 0.5)
ncideget('confnowledge.       k           ),
  'import'rce', souget('owledge.      kn          ent'],
    ontwledge['c       kno       ,
      e['topic']   knowledg                nowledge(
 ore_k  self.st       
       , []):wledge't('knodata.geport_dge in imfor knowle    e
        wledg Import kno     #                
     )
        
      tance', 1)impor('   conv.get                 ext'),
ontonv.get('c c            
       '),idn_et('sessio conv.g                   '],
s_responservionv['ja       c          nput'],
   ser_i  conv['u           
       on(e_conversatistor     self.      ):
     sations', []onveret('c.gtamport_daonv in i      for c
      versationsonport c        # Im     
 
          (f)n.load_data = jsort        impo        f:
  as_path, 'r')importh open(     witry:
       "
        tile""emory from fImport m""
        ") -> bool:ath: str, import_p_memory(self import  
    def ""
  urn    ret        ")
ry: {e}g memotin expor"❌ Error  print(f      s e:
    xception a  except E
              _path
     exportrn    retu
        th}")_pa {exportexported to: Memory nt(f"✅     pri
                  t=2)
 , indenort_data, fump(exp  json.d      
        s f:) a, 'w'port_pathth open(ex    wi          

          }       ()
     matow().isofortetime.nmp': dat_timestaxpor        'e
        ats,stmory_.mes': selftistic   'sta       ,
      ()rencesrefeget_user_pces': self.   'preferen           
  mit=1000),dge("", liknowleself.search_knowledge':       '      00),
    t=10mitions(lisae_converevself.retrisations':  'conver     
          ata = {    export_d             
    son"
   %H%M%S')}.j%m%d_time('%Yrfe.now().statetim_export_{ds_memory f"jarvih or export_patpath =rt_   expo
              try:""
   file"ory to xport mem"E        "") -> str:
ne No str =ath:f, export_pmory(selt_me  def expor    
  
"): {e}eanupory clng memr duri"❌ Erro print(f    
       ption as e: except Exce      
             ys")
_old} daayshan {des older ttrir ened foetanup compl Memory cle"✅t(fprin      
                 )
 ormat(w().isofetime.noanup'] = dat_cle_stats['lastoryelf.mem    s     tamp
   nup times Update clea  #         
          mit()
   onn.com c               
               date,))
 cutoff_  ''', (          = 0
    ess_count  acc3 ANDdence < 0. ? AND confimestamp <WHERE ti                    ledge 
OM knowLETE FRDE              ('''
      xecutesor.e        cur     
   fidenceone with low ced knowledgean unus       # Cl          
            date,))
   f_(cutof      ''',           rtance < 2
impo ? AND amp <HERE timest    W          
      ions M conversatFROLETE   DE             '''
     execute(ursor.       c         mportance
h low i wittions conversaean old     # Cl           
                sor()
r = conn.cur  curso           :
   ath) as connt(self.db_pte3.connecwith sqli             
        at()
   )).isoformldays_oelta(days=d - timedw()(datetime.nof_date =       cutof  
          try:"
  ""iestry enmemorlean up old ""C      "
  = 30):old: int (self, days_p_memoryef cleanu
    d    {}
urn        ret   {e}")
  references:  getting p"❌ Errorprint(f           as e:
 ption  Exceexcept  
                   s
   referenceurn p     ret         
             1]
     ow[0]] = rerences[row[     pref         :
      rowsn  irow  for            
                   nces = {}
re    prefe           etchall()
 .fcursor     rows =              
      ))
        d,, (user_i  '''     
         mp DESCstaER BY time    ORD            d = ?
    ERE user_i   WH           
      es preferencM         FRO      ue 
      eference_valype, prrence_tELECT prefe         S
           ute('''ursor.exec      c         ()
  conn.cursorrsor =       cu:
         onn_path) as cself.db3.connect(with sqlite             try:
"
       ferences""Get user pre      """ict:
  ult") -> D = "defatr user_id: sself,nces(refere get_user_pdef  
    1
  n -  retur         : {e}")
 eferenceg prError storinprint(f"❌            ion as e:
 xcept Except     e   
          d
      rn pref_i        retu
                  )
      onn.commit(        c    d
    .lastrowid = cursor pref_i                
         ))
      imestampnce_value, trefereence_type, p preferuser_id,   ''', (             , ?, ?)
ES (?, ?     VALU         mp)
      lue, timestavae_eferencce_type, prreferen (user_id, p                   es 
ncfere preINTOSERT  IN                   e('''
executursor.       c   or()
      .cursrsor = conn        cu:
        th) as connb_paf.donnect(sel.cith sqlite3     w  
              rmat()
   ofo.now().istimeatep = d timestam        try:
         "
  nce"" prefereStore user """   nt:
    t") -> i"defaulid: str =       user_           tr,
       e_value: senc preferstr,pe: ce_typreferene(self, referenctore_pef s   
    deturn {}
     r
        xt: {e}")etting conterror grint(f"❌ E      p   as e:
   xception  except E   
          ext
      return cont                   
)
     (user_inputionsiat_assoc.getlfons'] = seociati'asst[ex        conttions
     associa     # Get  
       
          ences()referuser_p= self.get_'] rencesefe['user_prext    cont
        cesenerrefer pet us # G               
       imit=3)
 nput, l_iuserwledge(.search_knolfge'] = seednt_knowlelevaontext['r    ce
         knowledgor relevant frchSea    #               
  imit)
    s(limit=lonversationf.retrieve_cns'] = selconversatioecent_t['rcontex            s
tionent conversarec  # Get    
                        }
      []
 ociations': 'ass            {},
    : rences'prefe      'user_  
        e': [],knowledgant_  'relev         [],
      sations':cent_conver      're
          ntext = {      cotry:
      
        """ responseseratingfor gent t context relevan"""Ge
        -> Dict:int = 5) r, limit: er_input: stse(self, usfor_respont_context_   def gese
    
 turn Fal       ree}")
     tion: {from interacrning r leant(f"❌ Erropri  
           as e:xceptionexcept E
               rue
     return T      
             nse)
     respout, jarvis_np(user_ins_associatioupdate       self.ns
     e associatio    # Updat    
        )
        ['value'], prefref['type']e(peferencstore_pr      self.    
      erences:ef pref in prfor       )
     uter_inperences(usextract_prefnces = self.ere       pref
     eferencesr pr Learn use   #   
            
           )     
      ence']onfidem['citdence=       confi          tion",
   racntesource="i                    tent'],
cont=item['nten co                  ],
 opic'=item['t topic               
    _knowledge(toref.s    sel            :
_itemsedge knowlm in for ite           
  
          )esponseis_rrv jainput,e(user__knowledgxtractms = self.enowledge_ite    k       ction
 terafrom inedge ial knowltent Extract po          #
          try:ck"""
feedbaions and ract inteusern from ear""L    "ol:
    > boone) -str = Nck: eedba       f                 str,
      nse: po, jarvis_resput: strinelf, user_ction(sm_interarn_frof lea
    de
       return []        )
 e}"wledge: { knohing searc"❌ Errort(f       prin
     n as e:eptio except Exc       
               ge_items
 turn knowled       re  
       nn.commit()          co       
               
ow[0]))oformat(), re.now().isimetat', (d        ''       ?
      WHERE id =                    = ?
     ssed1, last_access_count + = accecount  access_   SET            
         knowledge    UPDATE                      te('''
ecuursor.ex        c       
      countate access  # Upd                 
                           })
            row[7]
   ssed':t_acce       'las                 w[6],
 ross_count':     'acce                 
  ow[5],estamp': r       'tim          4],
       e': row[denc      'confi                  row[3],
    'source':                 2],
    nt': row[  'conte                 
     ic': row[1],       'top         ],
        ': row[0    'id              
      append({_items.edgenowl      k               rows:
ow in for r          
      = []wledge_items       kno
                
         )r.fetchall( cursos =       row 
                    )
    ', limit)query}% f'%{y}%',querf'%{     ''', (        ?
         LIMIT           C
     DESountC, access_cnfidence DESORDER BY co                 LIKE ?
   nt te con? ORLIKE WHERE topic                 
      knowledgeECT * FROM   SEL              '
   xecute(''.e      cursor        
  ext search)ll-tced with fu be enhanch (canxt searte# Simple              
                 sor()
  r = conn.cur      curso    
       as conn:f.db_path)onnect(selite3.cth sql         wi
       try:
    e"""wledge basSearch kno""      "t]:
  -> List[Dic 5) t: int =tr, limi, query: swledge(selfrch_knoea   def s    
 urn []
     ret
       e}")rsations: { convengievitrr re❌ Errot(f"       prin     s e:
eption axcept Exc        e    
         s
   conversationreturn        
                    })
                       []
   ] else]) if row[8ow[8oads(rson.l': j'tags                     row[7],
   ortance':     'imp                  [6],
  ': row 'sentiment                    {},
    w[5] elseif ro) w[5]son.loads(ro: j 'context'             
          ,ow[4]onse': rjarvis_resp   '                    ,
 3]': row[r_input   'use                   [2],
  owstamp': rme     'ti              
     [1],on_id': rowessi   's                     : row[0],
'id'               
         .append({onversations       c            
 s:w in rowro    for           ons = []
  ativers  con         
                    etchall()
  cursor.fs =    row           ams)
 arte(query, prsor.execu   cu                    
)
         pend(limit params.ap             ?'
   C LIMITtamp DES times= ' ORDER BY  query +          
                 ion_id)
   d(sesspen.ap    params          
      id = ?'ion_ND sessquery += ' A                 _id:
   ession       if s     
                    ]
hold_thresrtancempoarams = [i     p  
         ''        '?
        e >= importancERE  WH                  ions 
 atonversOM cFR* LECT      SE           
    ery = '''         qu        
        ()
       onn.cursor= ccursor                  as conn:
b_path)(self.dnnectte3.coith sqli w                try:
"
   ations""nverst cocen"Retrieve re ""
       ]:List[Dict -> t = 0)old: inhreshrtance_t      impo                    e,
   : str = Nonssion_id0, se: int = 1mitself, liions(nversatcoieve_  def retr
  
       return -1            : {e}")
  knowledgeringtorror snt(f"❌ E       pri        n as e:
 ceptio  except Ex            
         id
     nowledge_eturn k         r                
      s'] += 1
 ledge_entrieknow['_statslf.memoryse            s
    te statistic # Upda             
               
        }           
mestampp': titammes       'ti            ence,
 fide': con  'confidenc                  t,
 content':conten     '          e_id,
      knowledg 'id':                  ] = {
 [topic'semantic']emory_types[    self.m           
 c memorymantiAdd to se    #              
       
        it() conn.comm                  owid
 tr cursor.lasge_id =owled      kn                    
            )
  timestamp)amp, ence, timestnfidsource, co content, ''', (topic,                 ?)
    ?, ?,?, ?, ?,  (UES      VAL               
   cessed)p, last_acmestamnfidence, tisource, coent, , contpic        (to               e 
  knowledgINTO INSERT                   '
     ecute(''sor.ex      cur            rsor()
  onn.cusor = c    cur             nn:
   ath) as cob_pect(self.dite3.conn  with sql            
                 
 format()e.now().isodatetimamp =      timest
                  try:
     _lock: self.memory        with""
 base" knowledgethe in nowledge""Store k  "nt:
      ) -> i 0.8nce: float =ide       conf            ",
    "userrce: str = r, sou: sttr, contentpic: sge(self, toowleddef store_kn
     -1
     return    
           )ion: {e}"versating conr stornt(f"❌ Erro         pri     
  s e: Exception a except           
         _id
       sationturn conver       re
                      '] += 1
   nteractions'total_istats[elf.memory_        s   
     isticspdate stat        # U                
      )
     }           tance
   imporimportance':  '               sponse,
   : jarvis_rense'respos_vi 'jar                   er_input,
': us'user_input                 amp,
   estimmestamp': t    'ti           
     _id,rsation': conve      'id              append({
erm'].['short_try_typesmoelf.me    s      
       memoryt-term shorto   # Add           
                 commit()
         conn.        
     widlastroid = cursor.tion_ conversa           
                           
 tags))).dumps(      json                  
  nce, mporta, imentnti or {}), seontextps(c   json.dum                 
      s_response,arvi, jput user_instamp,timeession_id, '', (s        '   
         ?)?, ?, ?, ?, , ?, ?, S (?LUE  VA                      tags)
ce, , importanentiment  context, s                   
     is_response,nput, jarv user_imestamp,_id, ti    (session                   
 nversations  INTO co     INSERT              e('''
     cut.exe   cursor          r()
       rsoonn.cu cursor = c           
        onn: ch) asb_patlf.dnnect(seqlite3.co s       with
                       
  onse) jarvis_resp_input,serct_tags(u.extrags = self         tags
       xtract ta E #            
              t)
     (user_inpuntimentnalyze_seelf.a = ssentiment           )
     ementationle impl(simpntiment se  # Analyze              
              
   id()session_generate_ or self.ession_idion_id = sss       se)
         rmat(fo.now().isome datetiamp =esttim       
         try:     :
       y_lock.memorself  with   ""
    y"ion in memornversat"Store a co       "") -> int:
  = 1ce: intimportan                    
      ne,ct = Noext: DiNone, contid: str = on_     sessi                    
 , se: strresponvis_jar str, t:inpuer_lf, usation(seore_conversst  def 
    
  onn.commit()  c              
   
       ''')
                  )
        TEXTtimestamp                 AL,
    ngth REn_stressociatio           a       _b TEXT,
  ncept      co           T,
   a TEXoncept_   c               CREMENT,
  KEY AUTOINPRIMARY R    id INTEGE          (
        ociations EXISTS assOT IF NABLE    CREATE T      ('''
      .executeursor          cable
  ns tciatioemory asso # M      
                   ''')

                   )    
   _used TEXT   last                
 ,tamp TEXTtimes              
      FAULT 0, DEER_count INTEGage         us           ,
_rate REAL     success              a TEXT,
 atill_d      sk            
  XT,e TEaml_nskil                  T,
  MENOINCRE AUTRY KEYTEGER PRIMAIN         id 
           kills (S sXISTNOT ETE TABLE IF  CREA         ''
      ecute('.exursor  c         res table
 edulls and proc       # Ski 
              '')
    '                )
          TEXT
   timestamp                  XT,
 TEvalueference_   pre