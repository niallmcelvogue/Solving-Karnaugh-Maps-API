import React, {useEffect, useState} from 'react'
import styled from 'styled-components'
import { useTable, useRowSelect } from 'react-table'
import data from "./data";
import {Grid} from "@mui/material"
import axios from "axios"
import {FirstPairing, PITable} from "./PrimeImplicantTable";

const Styles = styled.div`
  padding: 1rem;

  table {
    border-spacing: 0;
    border: 1px solid black;

    tr {
      :last-child {
        td {
          border-bottom: 0;
        }
      }
    }

    th,
    td {
      margin: 0;
      padding: 0.5rem;
      border-bottom: 1px solid black;
      border-right: 1px solid black;

      :last-child {
        border-right: 0;
      }
    }
  }
`

const IndeterminateCheckbox = React.forwardRef(
  ({ indeterminate, ...rest }, ref) => {
    const defaultRef = React.useRef()
    const resolvedRef = ref || defaultRef

    React.useEffect(() => {
      resolvedRef.current.indeterminate = indeterminate
    }, [resolvedRef, indeterminate])

    return (
      <>
        <input type="checkbox" ref={resolvedRef} {...rest} />
      </>
    )
  }
)

function TruthTable({ columns, data }) {
    const [response, setResponse] = useState('')
    const [primeData, setPrimeData] = useState([])
    const [firstPairingData, setfirstPairingData] = useState([])
    const [secondPairingData, setSecondPairingData] = useState([])
    const [showPrimeTable, setShowPrimeTable] = useState(false)

    useEffect(() => {
        console.log(firstPairingData)
        if(firstPairingData.length > 0){
            console.log(true)
        }
    }, [firstPairingData])

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    state: { selectedRowIds },
  } = useTable(
    {
      columns,
      data,
    },
    useRowSelect,
    hooks => {
      hooks.visibleColumns.push(columns => [
        // Let's make a column for selection
          ...columns,
        {
          id: 'selection',
          // The header can use the table's getToggleAllRowsSelectedProps method
          // to render a checkbox
          Header: ({ getToggleAllRowsSelectedProps }) => (
            <div>
              <IndeterminateCheckbox {...getToggleAllRowsSelectedProps()} />
            </div>
          ),
          // The cell can use the individual row's getToggleRowSelectedProps method
          // to the render a checkbox
          Cell: ({ row }) => (
            <div>
              <IndeterminateCheckbox {...row.getToggleRowSelectedProps()} />
            </div>
          ),
        }
      ])
    }
  )

    const addInputHandler = (e) => {
        let input = Object.keys(selectedRowIds).join(' ')
        if (input) {
            axios.post('http://localhost:8000/solve', {
                'input': input,
                'noVar': 4,
                'type': e.target.id
            }, {withCredentials: true})
                .then(response => {
                    console.log(response.data.output)
                    if (response.data) {
                        setResponse(response.data.output[0])
                        setPrimeData(response.data.output[1])
                        setfirstPairingData(response.data.output[2])
                        setSecondPairingData(response.data.output[3])
                    } else {
                        Error()
                    }
                })
        }
        setShowPrimeTable(true)
    }

  // Render the UI for your table
  return (
      <Grid container spacing={2}>
        <Grid item xs={4}>
      <div>
    <div style={{'display':'block', 'width':'55%'}}>
      <table {...getTableProps()} style={{'marginTop': '60px'}}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}
                 style={{
                                'borderBottom': 'solid 3px red',
                                'background': 'aliceblue',
                                'color': 'black',
                                'fontWeight': 'bold',
                            }}
                >{column.render('Header')}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row, i) => {
            prepareRow(row)
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => {
                  return <td {...cell.getCellProps()}
                   style={{
                                        'padding': '10px',
                                        'border': 'solid 1px gray',
                                        'background': 'papayawhip',
                                        'width': "calc(100vw/2)",
                                    }}
                  >{cell.render('Cell')}</td>
                })}
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
          <div style={{'display':'flex'}}>
               <div style={{'marginTop':'10px'}}>
              <button id="SOP" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>SOP
            </button>
            <button id="POS" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>POS
            </button>
            <button id="NAND" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>NAND
            </button>
            <button id="NOR" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>NOR
            </button>
          </div>
          </div>
          </div>
        </Grid>
               <Grid item xs={6}>
                   <div style={{display:'inline-block'}}>
                   {showPrimeTable ? PITable(primeData) : null}
                   </div>
                   <div style={{display:'inline-block'}}>
                   {firstPairingData.length > 0 ? FirstPairing(firstPairingData) : null}
                   </div>
                   <div style={{display:'inline-block'}}>
                   {secondPairingData.length > 0 ? FirstPairing(secondPairingData) : null}
                   </div>
                   <div style={{display:'block'}}>
                       <h4>Optimised Solution {response.optimisedSolution}</h4>
                   </div>
               </Grid>
      </Grid>
  )
}
function MyTable() {
   const columns = React.useMemo(
        () => [
            {
                Header: 'A',
                accessor: 'A', // accessor is the "key" in the data
            },
            {
                Header: 'B',
                accessor: 'B',
            },
            {
                Header: 'C',
                accessor: 'C',
            },
            {
                Header: 'D',
                accessor: 'D',
            },
            {
                Header: 'Numeric',
                accessor: 'Numeric',
            }
        ],
       []
    )

  return (
    <Styles>
      <TruthTable columns={columns} data={data} />
    </Styles>
  )
}

export{
    MyTable,
    TruthTable
}
