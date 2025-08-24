/* Dashboard charts: line, bar and gauge-like doughnut */

function asCurrency(v){
  try { return new Intl.NumberFormat(undefined, {style:'currency', currency:'USD'}).format(v); } catch(e){ return v; }
}

export async function renderAdminCharts(){
  const txResp = await fetch('/dashboard/api/transactions/monthly/');
  const tx = await txResp.json();
  const ctxLine = document.getElementById('txChart');
  if(ctxLine){
    new Chart(ctxLine, { type:'line', data:{ labels:tx.labels, datasets:[{ label:'Volumes', data:tx.values, borderColor:'#ff8800', backgroundColor:'rgba(255,136,0,0.15)', tension:.35, fill:true }]}, options:{ plugins:{legend:{display:true}}, responsive:true, scales:{ y:{ beginAtZero:true } } });
  }

  const byTypeResp = await fetch('/dashboard/api/transactions/monthly-by-type/');
  const byType = await byTypeResp.json();
  const ctxBar = document.getElementById('typeChart');
  if(ctxBar){
    new Chart(ctxBar, { type:'bar', data:{ labels:byType.labels, datasets:[ {label:'Dépôts', data:byType.deposit, backgroundColor:'rgba(0,184,148,.7)'}, {label:'Retraits', data:byType.withdraw, backgroundColor:'rgba(255,99,132,.7)'} ] }, options:{ responsive:true, scales:{ y:{ beginAtZero:true } } });
  }

  const total = (tx.values||[]).reduce((a,b)=>a+b,0);
  const target = Math.max(1000, total*1.2);
  const gauge = document.getElementById('gauge');
  if(gauge){
    new Chart(gauge, { type:'doughnut', data:{ labels:['Atteint','Reste'], datasets:[{ data:[total, Math.max(0,target-total)], backgroundColor:['#ff8800','#e9ecef'] }] }, options:{ cutout:'70%', plugins:{legend:{display:false}, tooltip:{callbacks:{label:(c)=>asCurrency(c.parsed)}}} });
    const center = gauge.parentElement.querySelector('.gauge-center');
    if(center){ center.textContent = asCurrency(total); }
  }

  // Graphique de répartition des comptes par type
  const accountTypeResp = await fetch('/dashboard/api/account-types-distribution/');
  const accountTypeData = await accountTypeResp.json();
  const accountTypeCtx = document.getElementById('accountTypeChart');
  if(accountTypeCtx){
    new Chart(accountTypeCtx, { 
      type:'pie', 
      data:{ 
        labels:accountTypeData.labels, 
        datasets:[{
          data:accountTypeData.values, 
          backgroundColor:accountTypeData.colors,
          borderWidth: 2,
          borderColor: '#fff'
        }]
      }, 
      options:{ 
        responsive:true,
        plugins:{
          legend:{position:'bottom'},
          tooltip:{
            callbacks:{
              label: function(context) {
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((context.parsed / total) * 100).toFixed(1);
                return context.label + ': ' + context.parsed + ' comptes (' + percentage + '%)';
              }
            }
          }
        }
      } 
    });
  }

  // Graphique de croissance des clients
  const customerGrowthResp = await fetch('/dashboard/api/customer-growth/');
  const customerGrowthData = await customerGrowthResp.json();
  const customerGrowthCtx = document.getElementById('customerGrowthChart');
  if(customerGrowthCtx){
    new Chart(customerGrowthCtx, { 
      type:'line', 
      data:{ 
        labels:customerGrowthData.labels, 
        datasets:[{
          label:'Nombre de clients', 
          data:customerGrowthData.values, 
          borderColor:'#9C27B0', 
          backgroundColor:'rgba(156,39,176,0.1)', 
          tension:0.4, 
          fill:true,
          pointBackgroundColor: '#9C27B0',
          pointBorderColor: '#fff',
          pointBorderWidth: 2
        }]
      }, 
      options:{
        responsive:true, 
        scales:{y:{beginAtZero:true}},
        plugins:{
          legend:{display:true},
          tooltip:{
            callbacks:{
              label: function(context) {
                return 'Clients: ' + context.parsed.y;
              }
            }
          }
        }
      } 
    });
  }
}

export async function renderClientCharts(){
  // Graphique d'évolution du solde
  const balanceResp = await fetch('/dashboard/api/client/balance-evolution/');
  const balanceData = await balanceResp.json();
  const balanceCtx = document.getElementById('balanceChart');
  if(balanceCtx){
    new Chart(balanceCtx, { 
      type:'line', 
      data:{ 
        labels:balanceData.labels, 
        datasets:[{
          label:'Solde', 
          data:balanceData.values, 
          borderColor:'#4CAF50', 
          backgroundColor:'rgba(76,175,80,0.1)', 
          tension:0.4, 
          fill:true
        }]
      }, 
      options:{
        responsive:true, 
        scales:{y:{beginAtZero:true}},
        plugins:{
          legend:{display:true},
          tooltip:{
            callbacks:{
              label: function(context) {
                return 'Solde: ' + new Intl.NumberFormat('fr-FR', {style:'currency', currency:'EUR'}).format(context.parsed.y);
              }
            }
          }
        }
      } 
    });
  }

  // Graphique par type de transaction
  const typeResp = await fetch('/dashboard/api/client/transactions-by-type/');
  const typeData = await typeResp.json();
  const typeCtx = document.getElementById('typeChart');
  if(typeCtx){
    new Chart(typeCtx, { 
      type:'doughnut', 
      data:{ 
        labels:typeData.labels, 
        datasets:[{
          data:typeData.values, 
          backgroundColor:typeData.colors,
          borderWidth: 2,
          borderColor: '#fff'
        }]
      }, 
      options:{ 
        responsive:true,
        plugins:{
          legend:{position:'bottom'},
          tooltip:{
            callbacks:{
              label: function(context) {
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((context.parsed / total) * 100).toFixed(1);
                return context.label + ': ' + new Intl.NumberFormat('fr-FR', {style:'currency', currency:'EUR'}).format(context.parsed) + ' (' + percentage + '%)';
              }
            }
          }
        }
      } 
    });
  }

  // Graphique mensuel
  const monthlyResp = await fetch('/dashboard/api/transactions/monthly/');
  const monthlyData = await monthlyResp.json();
  const monthlyCtx = document.getElementById('monthlyChart');
  if(monthlyCtx){
    new Chart(monthlyCtx, { 
      type:'bar', 
      data:{ 
        labels:monthlyData.labels, 
        datasets:[{
          label:'Montants mensuels', 
          data:monthlyData.values, 
          backgroundColor:'rgba(33,150,243,0.7)',
          borderColor:'#2196F3',
          borderWidth: 1
        }]
      }, 
      options:{
        responsive:true, 
        scales:{y:{beginAtZero:true}},
        plugins:{
          tooltip:{
            callbacks:{
              label: function(context) {
                return 'Montant: ' + new Intl.NumberFormat('fr-FR', {style:'currency', currency:'EUR'}).format(context.parsed.y);
              }
            }
          }
        }
      } 
    });
  }

  // Graphique d'activité par heure
  const hourResp = await fetch('/dashboard/api/activity-by-hour/');
  const hourData = await hourResp.json();
  const hourCtx = document.getElementById('hourChart');
  if(hourCtx){
    new Chart(hourCtx, { 
      type:'bar', 
      data:{ 
        labels:hourData.labels, 
        datasets:[{
          label:'Activité', 
          data:hourData.values, 
          backgroundColor:'rgba(255,193,7,0.7)',
          borderColor:'#FFC107',
          borderWidth: 1
        }]
      }, 
      options:{
        responsive:true, 
        scales:{y:{beginAtZero:true}},
        plugins:{
          legend:{display:false}
        }
      } 
    });
  }

  // Jauge d'objectif d'épargne
  const savingsResp = await fetch('/dashboard/api/client/savings-progress/');
  const savingsData = await savingsResp.json();
  const savingsCtx = document.getElementById('savingsGauge');
  if(savingsCtx){
    new Chart(savingsCtx, { 
      type:'doughnut', 
      data:{ 
        labels:['Atteint','Reste'], 
        datasets:[{
          data:[savingsData.progress, 100-savingsData.progress], 
          backgroundColor:['#4CAF50','#e9ecef'],
          borderWidth: 0
        }]
      }, 
      options:{ 
        cutout:'70%', 
        plugins:{
          legend:{display:false}, 
          tooltip:{
            callbacks:{
              label:function(context) {
                if(context.dataIndex === 0) {
                  return 'Progression: ' + savingsData.progress.toFixed(1) + '%';
                }
                return '';
              }
            }
          }
        }
      } 
    });
    
    // Afficher le montant au centre
    const center = savingsCtx.parentElement.querySelector('.gauge-center');
    if(center){ 
      center.textContent = new Intl.NumberFormat('fr-FR', {style:'currency', currency:'EUR'}).format(savingsData.current);
    }
  }

  // Dernières transactions
  const recentResp = await fetch('/dashboard/api/client/recent-transactions/');
  const recentData = await recentResp.json();
  const recentEl = document.getElementById('recentTransactions');
  if(recentEl){
    if(recentData.items.length > 0) {
      recentEl.innerHTML = recentData.items.map(tx => `
        <div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #eee'>
          <div>
            <div style='font-weight:600; color:#333'>${tx.type} - ${tx.account}</div>
            <div style='font-size:0.9em; color:#666'>${tx.date} - ${tx.reference}</div>
            ${tx.description ? `<div style='font-size:0.8em; color:#999'>${tx.description}</div>` : ''}
          </div>
          <div style='font-weight:700; color:${tx.type === "DEPOSIT" ? "#4CAF50" : tx.type === "WITHDRAW" ? "#F44336" : "#2196F3"}'>
            ${tx.type === "WITHDRAW" ? "-" : "+"}${new Intl.NumberFormat('fr-FR', {style:'currency', currency:'EUR'}).format(tx.amount)}
          </div>
        </div>
      `).join('');
    } else {
      recentEl.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">Aucune transaction récente</div>';
    }
  }
}

