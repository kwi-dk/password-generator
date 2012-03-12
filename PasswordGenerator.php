#!/usr/bin/php
<?php
/**
 * Command-line password generator
 * -------------------------------
 *
 * Generates secure and random passwords guaranteed to satisfy the usual
 * complexity requirements as well.
 *
 * The generated passwords are of fixed length (currently 8), and guaranteed
 * to consist at least one characters from each of the defined character
 * categories (currently lower case, upper case and numbers).
 *
 * Homoglyphs (characters that look alike, such as "0" and "O") are not used.
 *
 * To estimate the entropy of generated passwords, run with -e argument.
 */

class PasswordGenerator
{
    /* Character categories */
    var $categories = array(
        'abcdefghjkmnopqrstuvwxyz',
        'ABCDEFGHJKLMNPQRSTUVWXYZ',
        '23456789',
     // '_-+*!.()=&',
    );

    /* Password length */
    var $length = 8;

    /**
     * Estimates total number of combinations.
     *
     * This does not account for the permutations of "forced" characters, so
     * the real number of combinations will be higher than this estimate.
     */
    function estimateCombinations()
    {
        $allCharsCount = 0;
        $combinations = 1;

        // Count combinations for the forced characters.
        foreach ($this->categories as $chars)
        {
            $combinations *= strlen($chars);
            $allCharsCount += strlen($chars);
        }

        // Multiply by combinations for the unforced characters.
        $combinations *= pow($allCharsCount, $this->length - count($this->categories));

        return $combinations;
    }

    function generatePassword()
    {
        $allCharacters = implode('', $this->categories);

        // Start with a password makeup where each character is picked freely among $allCharacters.
        $passwordMakeup = array_fill(0, $this->length, $allCharacters);

        // For each category, we now force one random character to be from that specific category.
        // If there are more categories than characters, we hang. :-)
        $forced = array_fill(0, $this->length, false);
        foreach ($this->categories as $chars)
        {
            while (true)
            {
                // Determine character index to force.
                $i = mt_rand(0, $this->length - 1);
                if (!$forced[$i])
                {
                    $forced[$i] = true; // Don't force the same character twice.
                    $passwordMakeup[$i] = $chars;
                    break;
                }
            }
        }

        $password = '';
        for ($i = 0; $i < $this->length; $i++)
        {
            $chars = $passwordMakeup[$i];
            $j = mt_rand(0, strlen($chars) - 1);
            $password .= $chars[$j];
        }
        return $password;
    }
}

/*
 * Command-line interface
 */
$g = new PasswordGenerator();

if ($argc == 2 && $argv[1] == '-e')
{
    $combinations = $g->estimateCombinations();
    printf("More than %s combinations ~ %.1f bits of entropy.\n", $combinations, log($combinations, 2));
    exit(0);
}

print($g->generatePassword() . "\n");
