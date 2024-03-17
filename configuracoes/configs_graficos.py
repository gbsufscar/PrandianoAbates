configs_lucro = {
  "title": {
    "text": 'R$'
  },
  "tooltip": {
    "trigger": 'axis'
  },
  "grid": {
    "left": '3%',
    "right": '4%',
    "bottom": '3%',
    "containLabel": True
  },
  "xAxis": {
    "type": 'category',
    "boundaryGap": False,
  },
  "yAxis": {
    "type": 'value'
  },
  "series": [
    {
      "name": 'Lucros',
      "type": 'line',
      "stack": 'Total',
      "markPoint": {
        "data": [
          { "type": 'max', "name": 'Max' }
        ]
      }
    }
  ]
}


configs_massas = {
  "title": {
    "text": ''
  },
  "tooltip": {
    "trigger": 'axis'
  },
  "legend": {
    "data": ["Massa Animal Registrada", "Massa de Ração Registrada", "Massa Animal Teórica", "Massa de Ração Teórica"],    
  },
  "grid": {
    "left": '3%',
    "right": '4%',
    "bottom": '3%',
    "containLabel": True
  },
  "xAxis": {
    "type": 'category',
    "boundaryGap": False,
  },
  "yAxis": {
    "type": 'value'
  },
  "series": [
    {
      "name": 'Massa Medida',
      "type": 'line',
    },
    {
      "name": 'Custo Medido',
      "type": 'line',
    }
  ]
}

