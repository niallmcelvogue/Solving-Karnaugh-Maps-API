import React, {useEffect, useState} from 'react'
import styled from 'styled-components'
import { useTable } from 'react-table'
import {Grid} from "@mui/material"
import key from 'weak-key';

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

function PrimeImplicantTable({ columns, data }) {
  // Use the state and functions returned from useTable to build your UI
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      columns,
      data,
    }
  )
  // Render the UI for your table
  return (
      <Grid container spacing={2}>
        <Grid item xs={4}>
      <div>
    <div style={{'display':'block', 'width':'110%'}}>
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
                  return <td {...cell.getCellProps()} key={cell.Binary}
                      style={{borderRight:'none'}}
                  >{cell.render('Cell')}</td>
                })}
              </tr>
            )
          })}
        </tbody>
      </table>
          </div>
          </div>
        </Grid>
      </Grid>
  )
}
function PITable (data) {
    const columns = [
        {
            Header: "Group",
            accessor: "Group"
        },
        {
            Header: "Binary",
            accessor: PrimeImplicantData => PrimeImplicantData.Binary.map(item => (
                <div>
                    <span>{item}</span>
                </div>
            ))
        },
        {
            Header: "Decimal",
            accessor: PrimeImplicantData => PrimeImplicantData.Decimal.map(item => (
                <div>
                    <span>{item}</span>
                </div>
            ))
        },

    ]

  return (
    <Styles>
      <PrimeImplicantTable columns={columns} data={data} />
    </Styles>
  )
}

function FirstPairing (data) {
    const columns = [
        {
            Header: "Group",
            accessor: "Group"
        },
        {
            Header: "Binary",
            accessor: PrimeImplicantData => PrimeImplicantData.Binary.map(item => (
                <div>
                    <span>{item}</span>
                </div>
            ))
        },
        {
            Header: "Pairs",
            accessor: PrimeImplicantData => PrimeImplicantData.Pairs.map(item => (
                <div>
                    <span>{item}</span>
                </div>
            ))
        },

    ]

  return (
    <Styles>
      <PrimeImplicantTable columns={columns} data={data}/>
    </Styles>
  )
}

export {
    PITable,
    FirstPairing
}
