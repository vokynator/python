
fun main(args: Array<String>) {
    println("Enter an number in [1..100]")
    val read = readLine()!!
    var number = read.toIntOrNull()
    if (number != null)  {
        println("factors of given number are: ${primeFactors(number)}")
    }
    else {
        println("you were supposed to enter number")
    }
}

fun primeFactors(number: Int): String {
    var number = number
    val prime_divisors: MutableList<Int> = mutableListOf()
    var i = 2
    while (i <= number) {
        while (number % i == 0) {
            prime_divisors.add(i)
            number /= i
        }
        i++
    }
    return prime_divisors.joinToString()
}