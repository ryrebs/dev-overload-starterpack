import React, {Component} from 'react';
import {
    Platform,
    StyleSheet,
    Text,
    View,
    TouchableOpacity,
    Button } from 'react-native';

export default class Calculator extends Component {

    static navigationOptions = {
        title: 'Calculator',
        headerStyle: {
            backgroundColor: '#f4511e',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
      };

        constructor() {
          super()
          this.state = {
            resultText: "",
            calculationText: ""
          }
          this.operationsList = ['<', '+', '-', '*', '/']
        }
      
        calculateResult() {
          const text = this.state.resultText
          this.setState({
            calculationText: eval(text)
          })
        }
      
        operate(operation) {
          console.log('Operation pressed: ', operation)
          switch(operation) {
            case '<':
              console.log("text:", this.state.resultText)
              // split the texts into array
              let text = this.state.resultText.split('')
              console.log("popped", text)
              text.pop() // pop one
              console.log(text)
              this.setState({
                resultText: text.join('') // array to text
              })
              break;
            case '+':
            case '-':
            case '*':
            case '/':
              const lastChar = this.state.resultText.split('').pop()
              // check if the lastChar is an operator
              // allow pressing '<' with index 0
              // do nothing if there's already an operator
              if(this.operationsList.indexOf(lastChar) > 0) return
              // do nothing if items are empty
              if (this.state.resultText == '') return
              
              // if its the first operator
              // concatenate it with the result
              this.setState({
                resultText: this.state.resultText + operation
              })
              break;
          }
        }
      
        validate() {
          console.log("validate")
          text = this.state.resultText;
          if (this.operationsList.indexOf(text.slice(-1)) > -1) {
            console.log("Invalid")
            return false
          } else {
            console.log("VALID")
          }
      
          return true
        }
      
        btnPress(text) {
          console.log("state:", this.state.resultText)
          console.log('Button press:', text)
          // calculate 
          if(text == '=') {
            return this.validate() && this.calculateResult(this.state.resultText)
          }
      
          // concatenate texts
          this.setState({
            resultText: this.state.resultText+text
          })
        }
        
        render() {
          // numbers
          let rows = []
          let nums = [[1,2,3], [4,5,6],[7,8,9],['.',0,'=']]
          
          for (let i=0; i < 4; i++) { // row
            let row = []
            for(let j = 0; j < 3; j++) { // columns
              row.push(
                <TouchableOpacity
                  key={nums[i][j]}
                  onPress={() => {this.btnPress(nums[i][j])}}
                  style={styles.btn}>
                      <Text style={styles.btnText}>{nums[i][j]}</Text>
                </TouchableOpacity>)
            }
            rows.push(<View style={styles.row}>{row}</View>)
          }
      
          //operations
          let operations = []
          for (let i = 0; i < 5; i++) {
            operations.push(
            <TouchableOpacity key={this.operationsList[i]}style={styles.btn} onPress={() => this.operate(this.operationsList[i])}>
                <Text style={[styles.btnText, styles.white]}>{this.operationsList[i]}</Text> 
            </TouchableOpacity>)
          }
      
          return (
            <View style={styles.container}>
              <View style={styles.result}>
                <Text style={styles.resultText}>{this.state.resultText}</Text>
              </View>
              <View style={styles.calculation}>
                <Text style={styles.calculationText}>{this.state.calculationText}</Text>
              </View>
              <View style={styles.buttons}>
                {/* Calc no.s 0 - 9 */}
                <View style={styles.numbers}>
                  {rows}
                </View>
                <View style={styles.operations}>
                 {operations}
                </View>
                <View style={styles.rightBorder}>
                </View>
              </View>
            </View>
          );
        }
      }
      
      const styles = StyleSheet.create({
        container: { // root container
          flex: 1,
          flexDirection: 'column' // default , vertical setup
        },
        result: { // spans a size of 2
          flex: 2,
          backgroundColor: 'white',
          justifyContent: 'center',
          alignItems: 'flex-end'
        },
        resultText: {
          fontSize: 30,
          color: 'black'
        },
        calculation: {
          flex: 1,
          backgroundColor: 'white',
          justifyContent: 'center',
          alignItems: 'flex-end'
        },
        calculationText: {
          fontSize: 24,
          color: 'black'
        },
        row: {
          flexDirection: 'row',
          flex: 1,
          justifyContent: 'space-around',
          alignItems: 'center'
        },
        buttons: { // root container for numbers and operations
          flex: 7,
          flexDirection: 'row' // setup elements in horizontal direction
        },
        btn: {
          flex: 1,
          alignItems: 'center',
          alignSelf: 'stretch',
          justifyContent: 'center'
        },
        btnText: {
          color: 'white',
          fontSize: 35
        },
        numbers: {
          flex: 5,
          backgroundColor: '#434343'
        },
        operations: {
          flex: 2,
          justifyContent: 'space-around',
          alignItems: 'stretch',
          backgroundColor: '#636363'
        },
        white: {
         color: 'white'
        },
        rightBorder: {
          flex: 0.5,
          backgroundColor: '#3366cc'
        }
});